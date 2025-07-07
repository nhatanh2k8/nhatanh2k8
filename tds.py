import importlib.util
import traceback
import os

# Đường dẫn tới file main.py nằm cùng thư mục
file_path = os.path.join(os.path.dirname(__file__), 'main.py')
module_name = 'main_module'

try:
    # Load file main.py như một module
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Gọi hàm Main() nếu tồn tại
    if hasattr(module, 'Main'):
        module.Main()
    else:
        print("⚠️ Không tìm thấy hàm Main trong main.py")

except Exception as e:
    print("❌ Đã xảy ra lỗi:")
    traceback.print_exc()

input("\n👉 Nhấn Enter để thoát...")
