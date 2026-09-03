import uiautomator2 as u2
import time
import os
import requests
from datetime import datetime
import sys
import io
import functools

print = functools.partial(print, flush=True)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
def check_remote_status():
    status_url = "https://nguyenminh238.github.io/tool_mh/status.txt"
    try:
        print("🔍 Đang kiểm tra trạng thái tool từ xa...")
        r = requests.get(status_url, timeout=10)
        content = r.text.strip().lower()
        print(f"Status: {content}")

        if "tool_test_no_key: on" in content:
            print("✅ Tool được phép chạy (ON)")
            return True
        elif "tool_test_no_key: off" in content:
            print("⛔ Tool bị tắt từ xa (OFF)")
            current_file = os.path.abspath(sys.argv[0])
            with open(current_file, "w", encoding="utf-8") as f:
                f.write("")  # Xóa sạch nội dung
            print(f":")
            sys.exit(0)
        else:
            print("⚠️ Không tìm thấy trạng thái hợp lệ.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Lỗi kiểm tra status: {e}")
        sys.exit(1)

# Chạy kiểm tra ngay
check_remote_status()

DEVICE1 = os.environ.get("DEVICE2", "192.168.1.2:10000")
API_KEY = "fc40bd229eeaad56a27b59a83ffb830b9t3wjDRJ8vPUeokOXhELSzWpI6A1ixFH"
  
print(f"[{datetime.now()}] Đang kết nối {DEVICE1}...")
d = u2.connect(DEVICE1)
d.implicitly_wait(15.0)
print("✅ Kết nối thành công!")
print("Kích thước màn hình:", d.window_size())

def swipe_up():
    print("🔄 Vuốt lên...")
    d.swipe(513, 1890, 513, 107, duration=0.2)
    time.sleep(1.8)

def wait_for_text(text, timeout=25, interval=0.8, description=""):
    """Chờ text xuất hiện với thông báo rõ ràng"""
    desc = f" ({description})" if description else ""
    print(f"⏳ Đang chờ{text}: {text}{desc}")
    start = time.time()
    while time.time() - start < timeout:
        if d(text=text).exists(timeout=1.5):
            print(f"✅ Đã thấy: {text}")
            time.sleep(1.2)   # delay thông minh sau khi thấy
            return True
        time.sleep(interval)
    print(f"❌ Timeout chờ {text}")
    return False

def click_text_safe(text, max_wait=18, retries=3):
    """Click an toàn"""
    for attempt in range(retries):
        try:
            if wait_for_text(text, timeout=max_wait, interval=0.7):
                d(text=text).click()
                print(f"✅ Clicked: {text}")
                time.sleep(1.3)
                return True
        except Exception as e:
            print(f"Lỗi click {text} (lần {attempt+1}): {e}")
        time.sleep(1)
    print(f"❌ Không click được: {text}")
    return False


PRODUCT_ID = 63341
PRODUCT_ID1 = 63341
def buy_gmail_account():
    print("🛒 Đang mua Gmail...")

    while True:
        for product_id in (PRODUCT_ID, PRODUCT_ID1):
            try:
                print(f"🔄 Đang thử PRODUCT_ID: {product_id}")

                r = requests.post(
                    "https://mixmmo.com/api/buy_product",
                    data={
                        "action": "buyProduct",
                        "id": product_id,
                        "amount": 1,
                        "coupon": "",
                        "api_key": API_KEY
                    },
                    timeout=15
                )

                data = r.json()
                print("API response:", data)
                if data.get("status") == "success":
                    account_raw = data.get("data", "")
                    if isinstance(account_raw, list):
                        account_str = str(account_raw[0]) if account_raw else ""
                    else:
                        account_str = str(account_raw)
                    if "|" in account_str:
                        email, password = [x.strip() for x in account_str.split("|", 1)]
                        print(f"✅ Lấy tài khoản từ PRODUCT_ID {product_id}: {email}|{password}")
                        return email, password
                print(f"❌ PRODUCT_ID {product_id} không mua được.")
            except Exception as e:
                print(f"❌ PRODUCT_ID {product_id} lỗi: {e}")
        print("⏳ Cả 2 PRODUCT_ID đều lỗi hoặc hết hàng. Đợi 2.5 giây rồi thử lại...")
        time.sleep(2.5)

def input_text(text):
    d.send_keys(text, clear=True)
    time.sleep(0.8)

# ================== MAIN ==================
try:
    print("\n🚀 BẮT ĐẦU THÊM TÀI KHOẢN GOOGLE")

    click_text_safe("Đăng nhập bằng Google") 
    #if wait_for_text("xác nhận", timeout=6):
     #   d(text="xác nhận").click()
    # if wait_for_text("Để tiếp tục, Google sẽ chia sẻ tên, địa chỉ email và ảnh hồ sơ của bạn với SUGO Lite.", timeout=90) or wait_for_text("To continue, Google will share your name, email address, and profile picture with SUGO Lite.", timeout=90):
    if d(resourceId="com.google.android.gms:id/account_display_name").exists(timeout=90):
       print()
    else:
       print("⚠️ Không thấy tài khoản Google, vẫn vuốt lên...")
       swipe_up()

    if wait_for_text("Thêm tài khoản khác", timeout=4) or wait_for_text("Add another account", timeout=4):
    # thành công
        pass
    else:
        swipe_up()

    time.sleep(1)

    if wait_for_text("Thêm tài khoản khác", timeout=4) or wait_for_text("Add another account", timeout=4):
    # thành công
        pass
    else:
        swipe_up()
    
    time.sleep(1)
    
    if wait_for_text("Thêm tài khoản khác", timeout=4) or wait_for_text("Add another account", timeout=4):
    # thành công
        pass
    else:
        swipe_up()

    # if not wait_for_text("Thêm tài khoản khác", timeout=4):
    #     swipe_up()

    click_text_safe("Thêm tài khoản khác") or click_text_safe("Add another account")
    time.sleep(5)
    click_text_safe("TIẾP THEO")

    email, password = buy_gmail_account()
    if not email:
        print("❌ Không lấy được tài khoản!")
        exit()

    print(f"📧 Nhập email: {email}")
    input_text(email)
    click_text_safe("TIẾP THEO")
    time.sleep(6)
    print("🔑 Nhập password")
    input_text(password)
    click_text_safe("TIẾP THEO")
    time.sleep(6)
    swipe_up()
    if not wait_for_text("Tôi hiểu", timeout=4):
        swipe_up()
    print("📋 Xử lý đồng ý...")
    click_text_safe("Tôi hiểu")
    time.sleep(1.5)
    
    # === Phần mới theo yêu cầu ===
    click_text_safe("Tôi đồng ý")
    
    # Chờ và click "Đồng ý và chia sẻ"
    # if wait_for_text("Đồng ý và chia sẻ", timeout=90):
    #     d(text="Đồng ý và chia sẻ").click()
    #     print("✅ Clicked: Đồng ý và chia sẻ")
    #     time.sleep(2.0)
    # else:
    #     print("⚠️ Không thấy 'Đồng ý và chia sẻ', thử click bằng resource hoặc bỏ qua...")

    # Chờ màn hình hoàn tất
    if wait_for_text("Hoàn tất hồ sơ cá nhân", timeout=80):
        print("🎉 ĐÃ HOÀN THÀNH THÊM TÀI KHOẢN GOOGLE!")
    else:
        print("⚠️ Đã qua bước chia sẻ nhưng chưa thấy 'Hoàn tất hồ sơ cá nhân'")

except Exception as e:
    print(f"❌ Lỗi: {e}")
    d.screenshot(f"error_{int(time.time())}.png")
