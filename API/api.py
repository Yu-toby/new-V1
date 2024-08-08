from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os  # 引入 os 模塊
import datetime as dt # 引入 datetime 模塊
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
# parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# UPLOAD_FOLDER = os.path.join(parent_folder, "uploads")
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
collection_temperature = db['temperature_threshold']
col_ori_identification_result = db['original_identification_result']
revise_collection = db['revise']
trained_collection = db['trained']
temp_collection = db['temperature_threshold']
col_if_retrain = db['if_retrain']
col_model_version = db['model_version']

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
        current_date = dt.date.today().strftime('%Y%m%d')
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
            time_record = dt.datetime.today().strftime('%Y%m%d-%H%M')
            collection_TimeRecord.update_one({}, {"$set": {"time_record": time_record}})

        # 插入數據到 MongoDB 
        result = collection_unidentified.insert_one({
            "time": dt.datetime.today().strftime('%Y%m%d-%H%M'),
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
@app.route('/tsmcserver/categories', methods=['GET', 'POST'])
def get_categories():    
    # 讀取時間紀錄
    if request.method == 'GET':
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
    
    elif request.method == 'POST':
        request_data = request.get_json()
        # date_start = request_data.get("date_start", "")
        # date_end = request_data.get("date_end", "")

        # 解析日期
        try:
            date_start, date_end = request_data["date_start"] + "-0000", request_data["date_end"] + "-2359"
        except ValueError as e:
            print("日期格式錯誤: ", e)
            # 處理錯誤，例如返回一個錯誤響應
            date_start = None
            date_end = None
        # print('date_start:', date_start, 'date_end:', date_end)

        query = {
            "time": {
                "$gte": date_start,
                "$lte": date_end
            }
        }

        matching_data = collection.find(query)
        # print('matching_data:', matching_data)

        # matching_data = collection.find({"time": time_record})
            
        # 檢查是否有匹配的數據
        if len(list(matching_data)) > 0:
            # 對匹配的數據執行 distinct 操作
            categories = matching_data.distinct("category")
            # print('categories:', categories)
            if not categories:
                return jsonify([])
            return jsonify(categories)
        # print('categories:', [])
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
            collection.find(search_criteria, projection={"original_id": False})
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

            data_item["_id"] = str(data_item["_id"])
            data_item["time"] = data_item.get("time", "")
            data_item["category"] = data_item.get("category", "")
            data_item["max"] = round(float(data_item.get("temp", {}).get("max", 0)), 1)
            data_item["avg"] = round(float(data_item.get("temp", {}).get("avg", 0)), 1)
            data_item["min"] = round(float(data_item.get("temp", {}).get("min", 0)), 1)
            data_item["result"] = data_item.get("result", "")
            data_item["thermal"] = f"data:image/jpeg;base64,{image_base64}"
            data_item["visible_light"] = data_item.get("image", {}).get("visible_light", "")
            data_item["original_image"] = image_path
            data_item["correction_mark"] = data_item.get("correction_mark", "")

        search_time_record = {"time": time_record}
        data1 = list(collection.find(search_time_record, projection={"original_id": False}))
        # print("data1:", data1)
        
        # 統計特定 category 對應四種 result 的數量
        category_count = defaultdict(lambda: {"正常": 0, "注意": 0, "異常": 0, "危險": 0})
        for item1 in data1:
            if category == "全部":
                category_count["全部"][item1["result"]] += 1
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
        # time_record = collection_TimeRecord.find_one().get("time_record", "")
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

        
        # print('search_criteria:', search_criteria)

        data2 = list(collection.find(projection={"original_id": False}))
        # print("data2:" , data2)

        # 查詢並回傳結果
        data = list(
            collection.find(search_criteria, projection={"_id": False, "original_id": False})
            .sort([("name", 1)])  # 依照 name 欄位升冪排序
            .skip(skip_count)
            .limit(pageSize)  # 限制回傳筆數
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

        # search_time_record = {"time": time_record}
        query = {
            "time": {
                "$gte": f"{start_mongodb_date}-0000",
                "$lte": f"{end_mongodb_date}-2359"
            }
        }
        data1 = list(collection.find(query, projection={"original_id": False}))
        # print("data1:", data1)
        
        # 統計特定 category 對應四種 result 的數量
        category_count = defaultdict(lambda: {"正常": 0, "注意": 0, "異常": 0, "危險": 0})
        for item1 in data1:
            if category == "全部":
                category_count["全部"][item1["result"]] += 1
            if item1["category"] == category:
                category_count[category][item1["result"]] += 1

        # print("category_count:", category_count)

        response_data = {"data": data, "category_count": category_count}
        # print("response_data:", response_data)
        return jsonify(response_data), 200
    

@app.route('/tsmcserver/getTemperatureArray', methods=['POST'])
def getTemperatureArray():
    if request.method == 'POST':
        request_data = request.get_json()

        # 提取搜尋條件
        name = request_data.get("name", "")
        result = request_data.get("result", "")
        print("name1:", name, "result:", result)

        # 在 MongoDB 中查找符合條件的資料
        temp_data = collection_temperature.find_one({"name": name})

        if not temp_data:
            return jsonify({"error": "找不到相應的"+ name + "資料"}), 404

        overall_tmp = temp_data.get("overall_tmp", [])
        normal_tmp = temp_data.get("normal_tmp", [])
        notice_tmp = temp_data.get("notice_tmp", [])
        abnormal_tmp = temp_data.get("abnormal_tmp", [])
        danger_tmp = temp_data.get("danger_tmp", [])
        # 根據 result 返回對應的 tmp
        if result == '正常':
            tmp = temp_data.get("normal_tmp", [])
        elif result == '注意':
            tmp = temp_data.get("notice_tmp", [])
        elif result == '異常':
            tmp = temp_data.get("abnormal_tmp", [])
        elif result == '危險':
            tmp = temp_data.get("danger_tmp", [])
        else:
            return jsonify({"error": "無效的 result"}), 400

        print("overall_tmp:", overall_tmp, "tmp:", tmp)
        # 回傳資料
        return jsonify({"overall_tmp": overall_tmp, "tmp": tmp, "normal_tmp": normal_tmp, "notice_tmp": notice_tmp, "abnormal_tmp": abnormal_tmp, "danger_tmp": danger_tmp}), 200

@app.route('/tsmcserver/identification_error', methods=['POST'])
def identification_error():
    if request.method == 'POST':
        request_data = request.get_json()

        # 提取要更新的 _id、資訊
        record_id = request_data.get("_id", "")
        correction_mark = request_data.get("correction_mark", "")

        if not record_id:
            return jsonify({"status": "error", "message": "_id is required"}), 400

        # 將 _id 轉換為 ObjectId 類型
        from bson.objectid import ObjectId
        try:
            object_id = ObjectId(record_id)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
        
        update_result = collection.update_one(
            {"_id": object_id},
            {"$set": {"correction_mark": correction_mark}}
        )

        if update_result.modified_count == 1:
            return jsonify({"status": "success"})

# 修正辨識結果========================================================================================================
# 未修改頁面-----------------
@app.route('/tsmcserver/unmodified_page_info', methods=['POST'])
def unmodified_page_info():
    if request.method == 'POST':
        request_data = request.get_json()

        # 提取搜尋條件
        current_page = request_data.get("currentPage", 1)
        if_mark = request_data.get("if_mark", False)
        img_name_search = request_data.get("img_name_search", "")
        time_record = collection_TimeRecord.find_one().get("time_record", "")

        # 計算要跳過的文件數
        skip_count = (current_page - 1) * 18

        # 根據 if_mark 設置過濾條件
        if if_mark:
            tsmc_data = collection.find({"correction_mark": True, "time": time_record})
            image_names = [data["image"]["thermal"] for data in tsmc_data if "image" in data and "thermal" in data["image"]]

            query = {
                "image_path": {"$in": image_names},
                "time": time_record,
                "if_revise": False
            }
        else:
            if img_name_search == "":
                query = {
                    "time": time_record,
                    "if_revise": False
                }
            else:
                query = {
                    "image_path": {"$regex": img_name_search, "$options": "i"},
                    "time": time_record,
                    "if_revise": False
                }

        # 查詢結果和總數量
        results = col_ori_identification_result.find(query).skip(skip_count).limit(18)
        total_count = col_ori_identification_result.count_documents(query)

        # 將結果轉換為list
        result_list = list(results)
        for result in result_list:
            result['_id'] = str(result['_id'])  # 將ObjectId轉換為字串

        response_data = {
            "data": result_list,
            "total_count": total_count
        }

        return jsonify(response_data), 200

@app.route('/tsmcserver/reviseResult', methods=['POST'])
def reviseResult():
    if request.method == 'POST':
        # 檢查 "revise" 集合是否存在
        if "revise" not in db.list_collection_names():
            # 如果不存在，創建 "revise" 集合
            db.create_collection("revise")

        request_data = request.get_json()
        # print("request_data:", request_data)

        # 更新original_identification_result裡面的if_revise為true
        record_id = request_data.get("original_id", "")
        if not record_id:
            return jsonify({"status": "error", "message": "original_id is required"}), 400
        
        from bson.objectid import ObjectId
        try:
            object_id = ObjectId(record_id)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
        
        result = col_ori_identification_result.update_one(
            {"_id": object_id},
            {"$set": {"if_revise": True}}
        )

        # 插入數據到revise集合
        result = revise_collection.insert_one({
            "time": dt.datetime.today().strftime('%Y%m%d-%H%M'),
            "original_id": request_data.get("original_id", ""),
            "image_path": request_data.get("image", ""),
            "result_dataset": request_data.get("result_dataset", ""),
            "if_train": False
        })

        if result.inserted_id:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error"})

# 已修改頁面-----------------
@app.route('/tsmcserver/already_edited_page_info', methods=['POST'])
def already_edited_page_info():
    if request.method == 'POST':
        request_data = request.get_json()

        # 提取搜尋條件
        current_page = request_data.get("currentPage", 1)
        img_name_search = request_data.get("img_name_search", "")
        time_record = collection_TimeRecord.find_one().get("time_record", "")

        # 計算要跳過的文件數
        skip_count = (current_page - 1) * 18

        # 設置查詢條件
        if img_name_search == "":
            query = {
                "if_train": False
            }
        else:
            query = {
                "image_path": {"$regex": img_name_search, "$options": "i"},
                "if_train": False
            }

        # 查詢結果和總數量
        results = revise_collection.find(query).skip(skip_count).limit(18)
        total_count = revise_collection.count_documents(query)

        # 將結果轉換為list
        result_list = list(results)
        for result in result_list:
            result['_id'] = str(result['_id'])  # 將ObjectId轉換為字串

        response_data = {
            "data": result_list,
            "total_count": total_count
        }

        return jsonify(response_data), 200
    
@app.route('/tsmcserver/updateResult', methods=['POST'])
def updateResult():
    if request.method == 'POST':
        # 檢查 "revise" 集合是否存在
        if "revise" not in db.list_collection_names():
            # 如果不存在，創建 "revise" 集合
            db.create_collection("revise")

        request_data = request.get_json()
        # print("request_data:", request_data)

        # 提取要更新的 _id
        record_id = request_data.get("_id", "")
        if not record_id:
            return jsonify({"status": "error", "message": "_id is required"}), 400

        # 將 _id 轉換為 ObjectId 類型
        from bson.objectid import ObjectId
        try:
            object_id = ObjectId(record_id)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        # 構建更新數據
        update_data = {
            "time": dt.datetime.today().strftime('%Y%m%d-%H%M'),
            "result_dataset": request_data.get("result_dataset", ""),
        }

        # 更新數據
        result = revise_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )

        if result.modified_count > 0:
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "No record updated"}), 404

@app.route('/tsmcserver/deleteResult', methods=['POST'])
def deleteResult():
    if request.method == 'POST':
        request_data = request.get_json()
        # print("request_data:", request_data)

        # 刪除revise集合中的指定數據
        # 更新original_identification_result裡面的if_revise為false
        record_id = request_data.get("_id", "")
        original_id = request_data.get("original_id", "")

        if not record_id:
            return jsonify({"status": "error", "message": "_id is required"}), 400
        elif not original_id:
            return jsonify({"status": "error", "message": "original_id is required"}), 400

        # 將 _id 和 original_id 轉換為 ObjectId 類型
        from bson.objectid import ObjectId
        try:
            record_object_id = ObjectId(record_id)
            original_object_id = ObjectId(original_id)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        # 刪除 revise 集合中的指定數據
        delete_result = revise_collection.delete_one({"_id": record_object_id})
        
        # 更新 original_identification_result 集合中的 if_revise 為 false
        update_result = col_ori_identification_result.update_one(
            {"_id": original_object_id},
            {"$set": {"if_revise": False}}
        )

        # 判斷刪除操作是否成功
        if delete_result.deleted_count == 0:
            return jsonify({"status": "error", "message": "No record deleted"}), 404

        # 判斷更新操作是否成功
        if update_result.modified_count == 0:
            return jsonify({"status": "error", "message": "Update failed"}), 500

        return jsonify({"status": "success"}), 200

@app.route('/tsmcserver/retrain', methods=['POST'])
def retrain():
    if request.method == 'POST':

        # 檢查 revise_collection 是否有資料
        documents = list(revise_collection.find({}))
        if not documents:
            return jsonify({"status": "error", "message": "No documents to transfer"}), 200

        # 檢查 "if_retrain" 集合是否存在
        if "if_retrain" not in db.list_collection_names():
            # 如果不存在，創建 "if_retrain" 集合，並插入一個初始文檔，"number" 設置為 0
            db.create_collection("if_retrain")
            db.if_retrain.insert_one({"number": 0})

        # 檢索當前 "number" 值
        current_document = db.if_retrain.find_one()
        if not current_document:
            return jsonify({"status": "error", "message": "No if_retrain document found"}), 404
        
        current_number = current_document.get("number", 0)
        # 切換 "number" 字段的值
        new_number = 1 if current_number == 0 else 1
        # 更新 "number" 字段的值
        db.if_retrain.update_one({}, {"$set": {"number": new_number}})

        # return jsonify({"status": "success", "new_number": new_number})

        # 更新每個文檔的 if_train 標籤為 true
        for document in documents:
            document['if_train'] = True

        # 將文檔插入 trained_collection
        insert_result = trained_collection.insert_many(documents)
        if len(insert_result.inserted_ids) != len(documents):
            return jsonify({"status": "error", "message": "Some documents were not inserted"}), 500

        # TODO: 是否要將數據刪除或保留

        # 刪除 revise_collection 中的所有文檔
        delete_result = revise_collection.delete_many({})
        if delete_result.deleted_count != len(documents):
            return jsonify({"status": "error", "message": "Some documents were not deleted"}), 500

        # # 保留 revise_collection 中的所有文檔
        # # 更新所有if_train為false的文檔為true
        # result = revise_collection.update_many(
        #     {"if_train": False},
        #     {"$set": {"if_train": True}}
        # )
        # if result.modified_count > 0:
        #     return jsonify({"status": "success", "updated_count": result.modified_count}), 200
        # else:
        #     return jsonify({"status": "error", "message": "No documents were updated"}), 404

        return jsonify({"status": "success", "message": "success", "transferred_count": len(documents), "if_train": new_number}), 200

# 已訓練頁面-----------------
@app.route('/tsmcserver/already_train_page_info', methods=['POST'])
def already_train_page_info():
    if request.method == 'POST':
        request_data = request.get_json()

        # 提取搜尋條件
        current_page = request_data.get("currentPage", 1)
        img_name_search = request_data.get("img_name_search", "")
        time_record = collection_TimeRecord.find_one().get("time_record", "")

        # 計算要跳過的文件數
        skip_count = (current_page - 1) * 18

        # 設置查詢條件
        if img_name_search == "":
            query = {}
        else:
            query = {
                "image_path": {"$regex": img_name_search, "$options": "i"}
            }

        # 查詢結果和總數量
        results = trained_collection.find(query).skip(skip_count).limit(18)
        total_count = trained_collection.count_documents(query)

        # 將結果轉換為list
        result_list = list(results)
        for result in result_list:
            result['_id'] = str(result['_id'])  # 將ObjectId轉換為字串

        response_data = {
            "data": result_list,
            "total_count": total_count
        }

        return jsonify(response_data), 200


@app.route('/tsmcserver/if_training', methods=['GET'])
def if_training():
    if request.method == 'GET':
        # 檢索當前 "number" 值
        current_document = db.if_retrain.find_one()
        if current_document:
            current_number = current_document.get("number", 0)
            return jsonify({"status": "success", "if_train": current_number})
        else:
            return jsonify({"status": "error"})

# 設定頁面========================================================================================================
# 溫度設定頁面-----------------
@app.route('/tsmcserver/temperature_page_info', methods=['POST'])
def temperature_page_info():
    if request.method == 'POST':
        # 查詢 temperature_threshold 集合中的所有文檔
        documents = list(temp_collection.find({}))

        if not documents:
            return jsonify({"status": "error", "message": "No documents found"}), 404

        # 重新整理資料
        result = []
        for document in documents:
            transformed_data = {
                "lowest_temperature": document.get("normal_tmp", [])[0],
                "temperature": [
                    document.get("normal_tmp", [])[1],
                    document.get("notice_tmp", [])[1],
                    document.get("abnormal_tmp", [])[1],
                    document.get("danger_tmp", [])[1]
                ],
                "device_type": document.get("name"),
                "_id": str(document.get("_id"))
            }
            result.append(transformed_data)

        return jsonify({"status": "success", "data": result}), 200
        
@app.route('/tsmcserver/update_temperature_data', methods=['POST'])
def update_temperature_data():
    if request.method == 'POST':
        request_data = request.get_json()
        print("request_data:", request_data)

        # 提取要更新的 _id
        record_id = request_data.get("_id", "")
        if not record_id:
            return jsonify({"status": "error", "message": "_id is required"}), 400

        # 將 _id 轉換為 ObjectId 類型
        try:
            object_id = ObjectId(record_id)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        # 構建更新數據
        lowest_temperature = request_data.get("lowest_temperature", 0)
        temperature_list = request_data.get("temperature", [])
        if len(temperature_list) != 4:
            return jsonify({"status": "error", "message": "temperature list must contain 4 elements"}), 400

        update_data = {
            "normal_tmp": [lowest_temperature, temperature_list[0]],
            "notice_tmp": [temperature_list[0], temperature_list[1]],
            "abnormal_tmp": [temperature_list[1], temperature_list[2]],
            "danger_tmp": [temperature_list[2], temperature_list[3]],
            "overall_tmp":temperature_list[3]
        }

        # 更新數據
        result = temp_collection.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )

        if result.modified_count > 0:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "No record updated"}), 404

@app.route('/tsmcserver/delete_temperature_data', methods=['POST'])
def delete_temperature_data():
    if request.method == 'POST':
        request_data = request.get_json()

        # 提取要刪除的 _id
        record_id = request_data.get("_id", "")
        if not record_id:
            return jsonify({"status": "error", "message": "_id is required"}), 400

        # 將 _id 轉換為 ObjectId 類型
        try:
            object_id = ObjectId(record_id)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        # 刪除數據
        result = temp_collection.delete_one({"_id": object_id})

        if result.deleted_count > 0:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "No record deleted"}), 404

# 模型板本設定頁面-----------------
@app.route('/tsmcserver/version_setting_page_info', methods=['POST'])
def version_setting_page_info():
    if request.method == 'POST':
        # 查詢 model_version 集合中的所有文檔
        documents = list(col_model_version.find({}))

        if not documents:
            return jsonify({"status": "error", "message": "No documents found"}), 404

        # 重新整理資料
        result = []
        for document in documents:
            transformed_data = {
                "_id": str(document.get("_id")),
                "model": document.get("model"),
                "version": document.get("version"),
                "P": document.get("P"),
                "R": document.get("R"),
                "mAP50": document.get("mAP50"),
                "using": document.get("using")
            }
            result.append(transformed_data)

        return jsonify({"status": "success", "data": result}), 200

@app.route('/tsmcserver/select_model_version', methods=['POST'])
def select_model_version():
    if request.method == 'POST':
        request_data = request.get_json()

        # 提取要更新的 _id
        record_id = request_data.get("_id", "")
        if not record_id:
            return jsonify({"status": "error", "message": "_id is required"}), 400

        # 將 _id 轉換為 ObjectId 類型
        try:
            object_id = ObjectId(record_id)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        # 將所有data的using設為false
        col_model_version.update_many({},{"$set": {"using": False}})

        # 構建更新數據
        update_data = {
            "using": True
        }

        # 更新數據
        result = col_model_version.update_one(
            {"_id": object_id},
            {"$set": update_data}
        )

        if result.modified_count > 0:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "No record updated"}), 404


@app.route('/tsmcserver/delete_model_version', methods=['POST'])
def delete_model_version():
    if request.method == 'POST':
        request_data = request.get_json()

        # 提取要刪除的 _id
        record_id = request_data.get("_id", "")
        if not record_id:
            return jsonify({"status": "error", "message": "_id is required"}), 400

        # 將 _id 轉換為 ObjectId 類型
        try:
            object_id = ObjectId(record_id)
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        # 刪除數據
        result = col_model_version.delete_one({"_id": object_id})

        if result.deleted_count > 0:
            return jsonify({"status": "success"}), 200
        else:
            return jsonify({"status": "error", "message": "No record deleted"}), 404



def create_indexes():
    # 為 'tsmccollection' 集合建立名字和狀態的索引
    collection.create_index([("name", 1), ("status", 1), ("time", 1)])
    col_ori_identification_result.create_index([("name", 1), ("status", 1), ("time", 1)])


if __name__ == '__main__':
    create_indexes()  # 在應用程式啟動之前建立索引
    app.run(debug=True, port=8000)