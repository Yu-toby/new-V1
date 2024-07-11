
# import subprocess
# import os

# def main():
#     # 切換到API目錄
#     api_dir = "C:\\Users\\WYC\\Desktop\\台積電熱影像\\Web\\new-V1\\API"
#     os.chdir(api_dir)

#     print(f"目前工作目錄: {os.getcwd()}")

#     # 執行 python api.py 指令
#     api_cmd = "python api.py"
#     api_process = subprocess.Popen(api_cmd, shell=True)

#     # 等待API啟動
#     # 這裡可以加入一些等待API啟動完成的邏輯，例如檢查特定端口是否被監聽

#     # 切換回項目目錄
#     project_dir = "C:\\Users\\WYC\\Desktop\\台積電熱影像\\Web\\new-V1"
#     os.chdir(project_dir)

#     print(f"切換回項目目錄: {os.getcwd()}")

#     # 執行其他指令（例如 npm run preview）
#     npm_preview_cmd = "npm run preview"
#     subprocess.run(npm_preview_cmd, shell=True)

# if __name__ == "__main__":
#     main()

import subprocess
import os

def main():
    # 獲取當前腳本所在的目錄
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    # 拼接API目錄的路徑
    api_dir = os.path.join(current_dir, "API")

    # 切換到API目錄
    os.chdir(api_dir)

    print(f"目前工作目錄: {os.getcwd()}")

    # 執行 python api.py 指令
    api_cmd = "python api.py"
    api_process = subprocess.Popen(api_cmd, shell=True)

    # 等待API啟動
    # 這裡可以加入一些等待API啟動完成的邏輯，例如檢查特定端口是否被監聽

    # 切換回原來的目錄
    os.chdir(current_dir)

    print(f"切換回項目目錄: {os.getcwd()}")

    # 執行其他指令（例如 npm run preview）
    npm_preview_cmd = "npm run preview"
    subprocess.run(npm_preview_cmd, shell=True)

if __name__ == "__main__":
    main()
