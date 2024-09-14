from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 设置 Chrome 调试模式
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "127.0.0.1:9222"

# 连接到已启动的 Chrome 浏览器
driver = webdriver.Chrome(options=chrome_options)

# 打开目标网页
driver.get('https://www.chinacodes.com.cn/exercises/gotoExercises.do')

def extract_questions(question_type):
    # 提取页面上的题目和选项
    questions = driver.find_elements(By.CLASS_NAME, 'des')
    print(f"\n{'='*10} {question_type} {'='*10}")
    for i, question in enumerate(questions):
        # 提取题目
        question_text = question.find_element(By.TAG_NAME, 'p').text
        print(f"题目: {question_text}")

        # 根据题型判断是否处理"正确/错误"选项
        if question_type == "判断题":
            # 提取判断题的选项
            options = question.find_elements(By.TAG_NAME, 'label')
            for j, option in enumerate(options):
                print(f"选项 {['正确', '错误'][j]}: {option.text.strip()}")
        else:
            # 提取单选或多选题的选项
            options = question.find_elements(By.TAG_NAME, 'li')
            for j, option in enumerate(options):
                print(f"选项 {chr(65 + j)}: {option.text.strip()}")

        # 提取正确答案
        try:
            correct_answer = question.find_element(By.XPATH, './/input[@class="cw"]').get_attribute('value')
            print(f"正确答案: {correct_answer}\n")
        except Exception as e:
            print(f"无法提取正确答案: {str(e)}")

# 定义一个函数来切换选项卡并提取题目
def switch_to_tab(xpath, question_type):
    # 点击选项卡
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    ).click()
    time.sleep(2)  # 给页面加载时间
    extract_questions(question_type)

# 爬取单项选择题
switch_to_tab('/html/body/div[2]/ul[1]/li[1]', "单选题")

# 爬取多项选择题
switch_to_tab('/html/body/div[2]/ul[1]/li[2]', "多选题")

# 爬取判断题
switch_to_tab('/html/body/div[2]/ul[1]/li[3]', "判断题")

print("所有题目爬取完成。")
