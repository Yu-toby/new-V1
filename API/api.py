from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os  # 引入 os 模塊
import datetime # 引入 datetime 模塊
from PIL import Image, ImageDraw
import io
import base64  # 引入 base64 模塊
from collections import defaultdict  # 引入 defaultdict 模塊
from datetime import datetime


app = Flask(__name__)
CORS(app)

def getEnvironmentVariable(key, default=None):
    try:
        env_key = os.environ[key] if default is None else os.environ.get(key, default)
        print("Set environment variable '{}' to '{}'.".format(key, env_key))
        return env_key
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(key)
        print(message)
        exit(1)

MONGO_HOST = getEnvironmentVariable('MONGO_HOST', "127.0.0.1")
MONGO_PORT = getEnvironmentVariable('MONGO_PORT', "27017")
MONGO_DBNAME = getEnvironmentVariable('MONGO_DBNAME', "tsmcdatabase")
mongo_uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"

app.config["SECRET_KEY"] = getEnvironmentVariable('SECRET_KEY',"")  # 自己用的時候改這樣：('SECRET_KEY',"")  給善淜：('SECRET_KEY')
UPLOAD_FOLDER = getEnvironmentVariable('UPLOAD_FOLDER', "uploads")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 連接到 MongoDB 數據庫
client = MongoClient(mongo_uri)
# db = client['TSMC_test']
# collection = db['detect_result']
db = client[MONGO_DBNAME]
collection = db['tsmccollection']

collection_unidentified = db['Unidentified']
collection1 = db['if_detect']
collection_TimeRecord = db['time_record']

# 確保上傳目錄存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 設定當前日期+順序的資料夾
file_count = 0

@app.route('/tsmcserver', methods=['GET', 'POST', 'DELETE'])
def todo():
    global current_folder
    global file_count

    if request.method == 'GET':
        # 從 MongoDB 讀取所有數據
        tsmcservers  = list(collection.find(projection = {"original_id":0}))

        if not tsmcservers:
            # 如果集合為空，返回一個空的 JSON 數組
            return jsonify([])

        for tsmcserver  in tsmcservers:
            # 獲取 X、Y 座標
            x1 = int(tsmcserver.get("coordinate", {}).get("xmin", 0))
            y1 = int(tsmcserver.get("coordinate", {}).get("ymin", 0))
            x2 = int(tsmcserver.get("coordinate", {}).get("xmax", 0))
            y2 = int(tsmcserver.get("coordinate", {}).get("ymax", 0))

            # 獲取圖片路徑
            image_path = tsmcserver.get("image", "")

            # 開啟圖片
            original_image = Image.open(os.getcwd() + "/" + image_path)

            # 創建一個可以繪製形狀的對象
            draw = ImageDraw.Draw(original_image)

            # 繪製方框
            draw.rectangle([x1, y1, x2, y2], outline='red', width=5)

            # 將圖像轉換為RGB模式
            if original_image.mode == 'RGBA':
                original_image = original_image.convert('RGB')

            # 將圖像轉換為Base64字串
            image_buffer = io.BytesIO()
            original_image.save(image_buffer, format='JPEG')
            image_base64 = base64.b64encode(image_buffer.getvalue()).decode()

            tsmcserver["_id"] = str(tsmcserver["_id"])
            tsmcserver["time"] = tsmcserver.get("time", "")
            tsmcserver["category"] = tsmcserver.get("category", "")
            tsmcserver["max"] = round(float(tsmcserver.get("temp", {}).get("max", 0)), 1)
            tsmcserver["avg"] = round(float(tsmcserver.get("temp", {}).get("avg", 0)), 1)
            tsmcserver["min"] = round(float(tsmcserver.get("temp", {}).get("min", 0)), 1)
            tsmcserver["result"] = tsmcserver.get("result", "")
            tsmcserver["image"] = f"data:image/jpeg;base64,{image_base64}"
            tsmcserver["original_image"] = image_path

        return jsonify(tsmcservers)

    elif request.method == 'POST':
        data = request.form.to_dict()
        # 處理圖片上傳
        images = request.files.getlist('image')

        # 檢查並更新 file_count
        current_date = datetime.date.today().strftime('%Y%m%d')
        new_filename = f'{current_date}-{str(file_count).zfill(3)}'

        while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], new_filename)):
            file_count += 1
            new_filename = f'{current_date}-{str(file_count).zfill(3)}'

        # 創建資料夾
        current_folder = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        os.makedirs(current_folder, exist_ok=True)

        image_filenames = []
        for image in images:
            file_path = os.path.join(current_folder, image.filename)
            image.save(file_path)
            image_filenames.append(file_path)

        data['images'] = image_filenames
        file_count += 1



        #檢查 "time_record" 集合是否存在
        if "time_record" not in db.list_collection_names():
            #如果不存在，創建 "time_record" 集合，並插入一個初始文檔，"time_record" 設置為 ""
            db.create_collection("time_record")
            db.time_record.insert_one({"time_record": ""})

        #更新時間紀錄
        time_record = collection_TimeRecord.find_one()
        if time_record:
            # time_record = time_record.get("time_record", "")
            time_record = datetime.datetime.today().strftime('%Y%m%d-%H%M')
            collection_TimeRecord.update_one({}, {"$set": {"time_record": time_record}})

        # 插入數據到 MongoDB 
        result = collection_unidentified.insert_one({
            "time": datetime.datetime.today().strftime('%Y%m%d-%H%M'),
            "image": image_filenames,
            "processed": False})
        
        if result.inserted_id:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"})

    elif request.method == 'DELETE':
        data = request.get_json()
        index = data['index']
        # 刪除數據
        result = collection.delete_one({"_id": ObjectId(index)})
        if result.deleted_count == 1:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "數據不存在"})

    return jsonify({"status": "error"})

# 新增一個路由來獲取 MongoDB 中的 "category" 選項
@app.route('/tsmcserver/categories', methods=['GET'])
def get_categories():    
    # 讀取時間紀錄
    time_record_document = collection_TimeRecord.find_one()
    
    if time_record_document:
        time_record = time_record_document.get("time_record", "")

        # 讀取與時間記錄相同時間的所有數據
        matching_data = collection.find({"time": time_record})
        
        # 檢查是否有匹配的數據
        if len(list(matching_data)) > 0:
            # 對匹配的數據執行 distinct 操作
            categories = matching_data.distinct("category")
            if not categories:
                return jsonify([])
            return jsonify(categories)

    return jsonify()

@app.route('/tsmcserver/if_detect', methods=['GET', 'POST'])
def if_detect():
    if request.method == 'GET':
        if_detect_number_document = collection1.find_one()

        if if_detect_number_document:
            if_detect_number = if_detect_number_document.get("number", 0)
            return jsonify(if_detect_number)
        else:
            # 如果集合為空，返回一個特定值或錯誤訊息
            return jsonify(0)
        
    elif request.method == 'POST':
        # 檢查 "if_detect" 集合是否存在
        if "if_detect" not in db.list_collection_names():
            # 如果不存在，創建 "if_detect" 集合，並插入一個初始文檔，"number" 設置為 0
            db.create_collection("if_detect")
            db.if_detect.insert_one({"number": 0})

        # 檢索當前 "number" 值
        current_document = db.if_detect.find_one()
        if current_document:
            current_number = current_document.get("number", 0)
            # 切換 "number" 字段的值
            new_number = 1 if current_number == 0 else 1
            # 更新 "number" 字段的值
            db.if_detect.update_one({}, {"$set": {"number": new_number}})

            return jsonify({"status": "success", "new_number": new_number})
        else:
            return jsonify({"status": "error"})
    
#讀取時間紀錄
@app.route('/tsmcserver/time_record', methods=['GET'])
def time_record():       
    if request.method == 'GET':
        time_record_document = collection_TimeRecord.find_one()
        
        if time_record_document:
            time_record = time_record_document.get("time_record", "")
            return jsonify(time_record)
        else:
            # 如果集合為空，返回一個特定值或錯誤訊息
            return jsonify({"status": "error", "message": "集合為空"})

@app.route('/tsmcserver/page_information', methods=['POST'])
def page_information():
    if request.method == 'POST':
        request_data = request.get_json()

        # 提取搜尋條件
        category = request_data.get("category", "")
        result = request_data.get("result", "")
        time_record = collection_TimeRecord.find_one().get("time_record", "")
        if result == "正常":
            page = request_data.get("nor_currentPage", 1)  # 如果未提供 'page' 參數，預設為第 1 頁
        elif result == "注意":
            page = request_data.get("not_currentPage", 1)
        elif result == "異常":
            page = request_data.get("abn_currentPage", 1)
        else:
            page = request_data.get("dan_currentPage", 1)
        
        # print(category, result, page)

        # 計算要跳過的文件數
        skip_count = (page - 1) * 18

        # 建立搜尋條件
        search_criteria = {}
        search_criteria["time"] = time_record
        if category != "全部":
            search_criteria["category"] = category

        if result != "全部":
            search_criteria["result"] = result
        # print('全部:', search_criteria)

        data2 = list(collection.find(projection={"original_id": False}))
        # print("data2:" , data2)

        # 查詢並回傳結果
        data = list(
            collection.find(search_criteria, projection={"_id": False, "original_id": False})
            .sort([("name", 1)])  # 依照 name 欄位升冪排序
            .skip(skip_count)
            .limit(18)  # 限制回傳筆數
        )        
        # print("data:")
        # for item in data:
        #     print(item)

        if not data:
            # 如果集合為空，返回一個特定值或錯誤訊息
            return jsonify({"status": "error", "message": "集合為空"})
                
        for data_item in data:
            # 獲取 X、Y 座標
            x1 = int(data_item.get("coordinate", {}).get("xmin", 0))
            y1 = int(data_item.get("coordinate", {}).get("ymin", 0))
            x2 = int(data_item.get("coordinate", {}).get("xmax", 0))
            y2 = int(data_item.get("coordinate", {}).get("ymax", 0))

            # 獲取圖片路徑
            image_path = data_item.get("image", {}).get("thermal", "")

            # 開啟圖片
            original_image = Image.open(os.getcwd() + "/" + image_path)

            # 創建一個可以繪製形狀的對象
            draw = ImageDraw.Draw(original_image)

            # 繪製方框
            draw.rectangle([x1, y1, x2, y2], outline='red', width=5)

            # 將圖像轉換為RGB模式
            if original_image.mode == 'RGBA':
                original_image = original_image.convert('RGB')

            # 將圖像轉換為Base64字串
            image_buffer = io.BytesIO()
            original_image.save(image_buffer, format='JPEG')
            image_base64 = base64.b64encode(image_buffer.getvalue()).decode()

            data_item["time"] = data_item.get("time", "")
            data_item["category"] = data_item.get("category", "")
            data_item["max"] = round(float(data_item.get("temp", {}).get("max", 0)), 1)
            data_item["avg"] = round(float(data_item.get("temp", {}).get("avg", 0)), 1)
            data_item["min"] = round(float(data_item.get("temp", {}).get("min", 0)), 1)
            data_item["result"] = data_item.get("result", "")
            data_item["thermal"] = f"data:image/jpeg;base64,{image_base64}"
            data_item["visible_light"] = data_item.get("image", {}).get("visible_light", "")
            data_item["original_image"] = image_path

        search_time_record = {"time": time_record}
        data1 = list(collection.find(search_time_record, projection={"original_id": False}))
        # print("data1:", data1)
        
        # 統計特定 category 對應四種 result 的數量
        category_count = defaultdict(lambda: {"正常": 0, "注意": 0, "異常": 0, "危險": 0})
        for item1 in data1:
            if item1["category"] == category:
                category_count[category][item1["result"]] += 1

        # print("category_count:", category_count)

        response_data = {"data": data, "category_count": category_count}
        # print("response_data:", response_data)
        return jsonify(response_data), 200
    
@app.route('/tsmcserver/status_number', methods=['POST'])
def number_information():
    if request.method == 'POST':
        request_data = request.get_json()

        # 提取搜尋條件
        category = request_data.get("category", "")
        time_record = collection_TimeRecord.find_one().get("time_record", "")

        # 建立搜尋條件
        if category == "全部":
            search_number = {"time": time_record}
        else:
            search_number = {"category": category, "time": time_record}
        # print('search_number:', search_number)
        data1 = list(
            collection.find(search_number, projection={"original_id": False}))
        # print("data1:", data1)
        
        # 統計特定 category 對應四種 result 的數量
        category_count = defaultdict(lambda: {"正常": 0, "注意": 0, "異常": 0, "危險": 0})
        for item1 in data1:
            if category == "全部":
                category_count["全部"][item1["result"]] += 1
            if item1["category"] == category:
                category_count[category][item1["result"]] += 1

        print("category_count1:", category_count)
        
        return jsonify(category_count), 200

@app.route('/tsmcserver/history_page_information', methods=['POST'])
def history_page_information():
    if request.method == 'POST':
        request_data = request.get_json()

        # 提取搜尋條件
        category = request_data.get("category", "")
        result = request_data.get("result", "")
        time_record = collection_TimeRecord.find_one().get("time_record", "")
        current_page = request_data.get("currentPage", 1)
        pageSize = request_data.get("pageSize", 20)
        date_start = str(request_data.get("date_start", ""))
        date_end = str(request_data.get("date_end", ""))

        # print('date: ', (date_start), (date_end))

        # 計算要跳過的文件數
        skip_count = (current_page - 1) * pageSize

        # 建立搜尋條件
        search_criteria = {}
        if date_start and date_end:
            # 將使用者輸入的日期轉換成 datetime 物件
            start_datetime = datetime.strptime(date_start, "%Y%m%d")
            end_datetime = datetime.strptime(date_end, "%Y%m%d")

            # 進行 MongoDB 內的時間格式轉換，並只取日期部分
            start_mongodb_date = start_datetime.strftime("%Y%m%d")
            end_mongodb_date = end_datetime.strftime("%Y%m%d")

            # 使用 MongoDB 內的時間格式進行範圍搜尋
            search_criteria["time"] = {
                "$gte": f"{start_mongodb_date}-0000",
                "$lte": f"{end_mongodb_date}-2359"
            }

        if category != "全部":
            search_criteria["category"] = category

        if result != "全部":
            search_criteria["result"] = result

        
        print('search_criteria:', search_criteria)

        data2 = list(collection.find(projection={"original_id": False}))
        # print("data2:" , data2)

        # 查詢並回傳結果
        data = list(
            collection.find(search_criteria, projection={"_id": False, "original_id": False})
            .sort([("name", 1)])  # 依照 name 欄位升冪排序
            .skip(skip_count)
            .limit(pageSize)  # 限制回傳筆數
        )        
        print("data:")
        for item in data:
            print(item)

        if not data:
            # 如果集合為空，返回一個特定值或錯誤訊息
            return jsonify({"status": "error", "message": "集合為空"})
                
        for data_item in data:
            # 獲取 X、Y 座標
            x1 = int(data_item.get("coordinate", {}).get("xmin", 0))
            y1 = int(data_item.get("coordinate", {}).get("ymin", 0))
            x2 = int(data_item.get("coordinate", {}).get("xmax", 0))
            y2 = int(data_item.get("coordinate", {}).get("ymax", 0))

            # 獲取圖片路徑
            image_path = data_item.get("image", {}).get("thermal", "")

            # 開啟圖片
            original_image = Image.open(os.getcwd() + "/" + image_path)

            # 創建一個可以繪製形狀的對象
            draw = ImageDraw.Draw(original_image)

            # 繪製方框
            draw.rectangle([x1, y1, x2, y2], outline='red', width=5)

            # 將圖像轉換為RGB模式
            if original_image.mode == 'RGBA':
                original_image = original_image.convert('RGB')

            # 將圖像轉換為Base64字串
            image_buffer = io.BytesIO()
            original_image.save(image_buffer, format='JPEG')
            image_base64 = base64.b64encode(image_buffer.getvalue()).decode()

            data_item["time"] = data_item.get("time", "")
            data_item["category"] = data_item.get("category", "")
            data_item["max"] = round(float(data_item.get("temp", {}).get("max", 0)), 1)
            data_item["avg"] = round(float(data_item.get("temp", {}).get("avg", 0)), 1)
            data_item["min"] = round(float(data_item.get("temp", {}).get("min", 0)), 1)
            data_item["result"] = data_item.get("result", "")
            data_item["thermal"] = f"data:image/jpeg;base64,{image_base64}"
            data_item["visible_light"] = data_item.get("image", {}).get("visible_light", "")
            data_item["original_image"] = image_path

        search_time_record = {"time": time_record}
        data1 = list(collection.find(search_time_record, projection={"original_id": False}))
        # print("data1:", data1)
        
        # 統計特定 category 對應四種 result 的數量
        category_count = defaultdict(lambda: {"正常": 0, "注意": 0, "異常": 0, "危險": 0})
        for item1 in data1:
            if item1["category"] == category:
                category_count[category][item1["result"]] += 1

        # print("category_count:", category_count)

        response_data = {"data": data, "category_count": category_count}
        # print("response_data:", response_data)
        return jsonify(response_data), 200
    

def create_indexes():
    # 為 'tsmccollection' 集合建立名字和狀態的索引
    collection.create_index([("name", 1), ("status", 1), ("time", 1)])


if __name__ == '__main__':
    create_indexes()  # 在應用程式啟動之前建立索引
    app.run(debug=True, port=8000)