from hanspell import spell_checker
import tkinter.ttk
import tkinter.font
import re
import webbrowser

window=tkinter.Tk()

window.title("생기부 도우미 by 광철 30313 한건희")
window.geometry("1040x680+50+10")
window.resizable(True, True)

# 생기부 금지어 리스트 (리스트 목록 받아서 기능 추가하기)
forbidden_words = ["광양제철고", "제철고", "제고", "광철고", "한빛", "모의고사", "포스", "POS", "전남",
                   "전라도", "광양", "영재", "논문", "보고서", "출판", "출간", "책쓰기", "발간", "대학교",
                   "외국", "해외", "어학", "연수", "교외", "수상", "대회", "표창", "발명", "특허", "출원",
                   "인증", "ebs", "EBS", "ted", "TED", "토익", "토플", "텝스", "한자급수시험", "개더타운",
                   "게더타운", "유튜브", "K-MOOC", "장학", "자격증", "방과후", "MOOC", "KOCW", "G리그",
                   "포스테드", "POSTED", "포스레보", "POSREVO", "포스코", "POSCO", "posco", "Posco",
                   "방과후", "방과후학교", "어학시험", "장학금", "장학", "네이버", "구글", "네이버밴드", "구글클래스룸",
                   "네이버 밴드", "구글 클래스룸", "유튜버", "UN", "유네스코", "커리어넷", "메이저맵", "반크", "제페토",
                   "아이폰", "KTX", "SRT", "패들렛", "띵커벨", "미리캔버스", "망고보드", "인스타그램", "페이스북",
                   "카카오톡", "카톡", "단톡"]

all_words = []

# 폰트
bold_font=tkinter.font.Font(family="맑은 고딕", size=20, slant="roman")
sub_font=tkinter.font.Font(family="맑은 고딕", size=15, slant="roman")
simple_font=tkinter.font.Font(family="맑은 고딕", size=13, slant="roman")

# 함수
def open_website():
    url = "http://speller.cs.pusan.ac.kr/"
    webbrowser.open(url)

def open_banned_word_image():
    url = "https://drive.google.com/file/d/1Mc3K-gySNDXoYKjhjH4deRfNXCjtw_2U/view?usp=drivesdk"
    webbrowser.open(url)

"""
def highlight_differences():
    text1_content = entry_before_check.get("1.0", "end-1c")  # 첫 번째 text 위젯의 내용
    text2_content = entry_fixed_txt.get("1.0", "end-1c")  # 두 번째 text 위젯의 내용

    # 기존에 설정된 태그 제거
    entry_fixed_txt.tag_remove("highlight", "1.0", "end")

    # 단어 단위로 비교하여 하이라이트 표시
    words1 = text1_content.split()
    words2 = text2_content.split()

    print(text1_content)
    print(words1)
    print(words2)

    for word1, word2 in zip(words1, words2):
        if word1 != word2:
            start = entry_fixed_txt.search(word2, "1.0", stopindex="end", count=tkinter.END)
            end = f"{start}+{len(word2)}c"
            entry_fixed_txt.tag_add("highlight", start, end)

    # 하이라이트 표시를 위한 태그 설정
    entry_fixed_txt.tag_config("highlight", background="green")
"""

def highlight_word(word2search, color, textbox): # red, lightblue, orange, green
    user_input = str(word2search)  # 검색할 문자
    text_content = entry_before_check.get("1.0", "end-1c")  # text 위젯의 전체 내용

    # 기존에 설정된 태그 제거
    # entry_before_check.tag_remove("highlight", "1.0", "end")

    # 입력 받은 단어 찾기
    if textbox == "input_text":
        start = "1.0"
        while True:
            start = entry_before_check.search(user_input, start, stopindex="end")
            if not start:
                break

            end = f"{start}+{len(user_input)}c"
            entry_before_check.tag_add("highlight_input", start, end)
            start = end

    elif textbox == "output_text":
        start = "1.0"
        while True:
            start = entry_fixed_txt.search(user_input, start, stopindex="end")
            if not start:
                break

            end = f"{start}+{len(user_input)}c"
            entry_fixed_txt.tag_add("highlight_output", start, end)
            start = end

    # 하이라이트 표시를 위한 태그 설정
    if textbox == "input_text":
        if color == "red":
            entry_before_check.tag_config("highlight_input", background="red")
        elif color == "orange":
            entry_before_check.tag_config("highlight_input", background="orange")
        elif color == "green":
            entry_before_check.tag_config("highlight_input", background="green")

    elif textbox == "output_text":
        if color == "red":
            entry_fixed_txt.tag_config("highlight_output", background="red")
        elif color == "orange":
            entry_fixed_txt.tag_config("highlight_output", background="orange")
        elif color == "green":
            entry_fixed_txt.tag_config("highlight_output", background="green")

def count():
    linespace_count = 0
    count_txt = count_textbox.get("1.0", tkinter.END)
    for i in count_txt:
        if "\n" in i:
            linespace_count += 1
    counted_number = len(str(count_txt)) - 1
    txt_bytes = len(str(count_txt).encode()) - 2 + linespace_count
    count_result_txt.config(text=f'▶ {txt_bytes}바이트, 공백 포함 {counted_number}자')

def check_spell():
    enter_removed_original_txt = ""
    forbidden_txt.delete("1.0", tkinter.END)
    spell_error_txt.delete("1.0", tkinter.END)

    original_txt = entry_before_check.get("1.0", tkinter.END)
    if "\n" in original_txt:
        enter_removed_original_txt = original_txt.replace("\n", "")

    # print(original_txt)
    # print(enter_removed_original_txt)

    new_str = []
    cut = 100
    for i in range(0, 100):
        new_str.append(enter_removed_original_txt[cut * i:cut * i + (cut)])
    # print(new_str)
    no_empty_new_str = list(filter(None, new_str))
    # print(no_empty_new_str)

    joined_str = ""
    errors = 0
    checked_splitted_list = []
    detected_words_list = []
    for i in no_empty_new_str:
        splitted_result = spell_checker.check(i.encode("utf-8"))
        errors += splitted_result.errors

        checked_splitted_list.append(splitted_result.checked)

        for k, v in splitted_result.words.items():
            if v == 1 or v == 2:
                detected_words_list.append(str(k))
                joined_str += str(k)
                joined_str += ", "

        # print(splitted_result.checked)
        if "<end>" in joined_str:
            joined_str = re.sub('<end>', '', joined_str)
        if "<br>" in joined_str:
            joined_str = re.sub('<br>', '', joined_str)
        if "&quot;" in joined_str:
            joined_str = re.sub('&quot;', '', joined_str)

    # print(detected_words_list)
    summed_str = ""
    for i in checked_splitted_list:
        summed_str += str(i)
    # print(summed_str)

    #기재 금기어 하이라이트
    for i in forbidden_words:
        if enter_removed_original_txt.find(i) != -1:
            highlight_word(i, "red", "input_text")
            forbidden_txt.insert("current", i)
            forbidden_txt.insert("current", ", ")

    entry_fixed_txt.delete("1.0", tkinter.END)
    entry_fixed_txt.insert("1.0", summed_str)

    changed_number_txt.config(text = f'▶ 수정한 사항: {errors}개')

    spell_error_txt.insert("1.0", joined_str)
    
    # 맞춤법 수정 하이라이트
    # highlight_differences()
    # for i in detected_words_list:
    #     if enter_removed_original_txt.find(i) != -1:
    #         highlight_word(i, "green", "output_text")

# 창 분할
notebook = tkinter.ttk.Notebook(window, width=1040, height=680)
notebook.pack()

# 1번 창 생성
frame1_1 = tkinter.Frame(window)
notebook.add(frame1_1, text="맞춤법 검사 및 기재 금기어 확인")

# 1번 창 구성 요소들
title_txt = tkinter.Label(frame1_1, text="맞춤법/기재 금기어 검사기", font=bold_font)
title_txt.pack(pady=10)

notice_txt = tkinter.Label(frame1_1, text="※ 맞춤법 검사 기능은 작동하나, 정확성은 보장할 수 없으므로 옆의 버튼을 눌러 사용하시기 바랍니다. (금기어 기능은 작동함)",
                           bg="darkorange")
notice_txt.pack(pady=1)

openweb_button=tkinter.Button(frame1_1, text="검사사이트 이동", command=open_website)
openweb_button.place(x=900, y=55)

input_txt = tkinter.Label(frame1_1, text="▼ 검사할 내용 입력 ▼")
input_txt.pack(pady=10)

entry_before_check = tkinter.Text(frame1_1, width=100, height=10, spacing2=5)
entry_before_check.pack(pady=5)
entry_before_check.insert(tkinter.END, "검사할 내용을 입력하세요.")

changed_number_txt = tkinter.Label(frame1_1, text="▶ 수정한 사항: ")
changed_number_txt.pack(pady=5)

inside_frame1_1 = tkinter.Frame(frame1_1, width=50, height=4, relief='solid', bd=2, bg='grey')
inside_frame1_1.pack(pady=10)

spell_error_txt = tkinter.Text(inside_frame1_1, width=50, height=4, spacing2=5)
spell_error_txt.pack(pady=10, side='left')
spell_error_txt.insert("1.0", "맞춤법 오류")

forbidden_txt = tkinter.Text(inside_frame1_1, width=50, height=4, spacing2=5)
forbidden_txt.pack(pady=10, side='right')
forbidden_txt.insert("1.0", "감지된 기재 금지어")

output_txt = tkinter.Label(frame1_1, text="▼ 맞춤법 수정된 내용 ▼")
output_txt.pack(pady=10)

entry_fixed_txt = tkinter.Text(frame1_1, width=100, height=10, spacing2=5)
entry_fixed_txt.pack(pady=5)
entry_fixed_txt.insert(tkinter.END, "검사 결과")

check_button=tkinter.Button(frame1_1, text="검사하기", command=check_spell)
check_button.pack(pady=5)

# 2번 창 생성
frame2=tkinter.Frame(window)
notebook.add(frame2, text="바이트/글자수 세기")

# 2번 창 구성 요소들
title_txt2=tkinter.Label(frame2, text="바이트/글자수 세기", font=bold_font)
title_txt2.pack(pady=10)

count_result_txt=tkinter.Label(frame2, text="▶진로활동: 2100바이트, 약 700자 || "
                                            "▶자율활동: 1500바이트, 약 500자 || "
                                            "▶동아리활동: 1500바이트, 약 500자 || "
                                            "\n ▶과목별세부능력특기사항: 1500바이트, 약 500자 || "
                                            "▶행동특성및종합의견: 1500바이트, 약 500자"
                                            "\n \n영어, 숫자, 특수문자, 띄어쓰기 1바이트 / 엔터키 2바이트 / 한글 3바이트")
count_result_txt.pack(pady=5)

count_textbox = tkinter.Text(frame2, width=100, height=25, spacing2=5)
count_textbox.pack(pady=20)
count_textbox.insert(tkinter.END, "내용을 입력하세요.")

count_button=tkinter.Button(frame2, text="검사하기", command=count)
count_button.pack(pady=10)

count_result_txt=tkinter.Label(frame2, text="▶ 바이트, 자", font = sub_font)
count_result_txt.pack(pady=5)

# 3번 창 생성
frame3=tkinter.Frame(window)
notebook.add(frame3, text="도움말 및 유의사항")

# 3번 창 구성 요소들
title_txt3 = tkinter.Label(frame3, text="도움말 및 유의사항", font=bold_font)
title_txt3.pack(pady=10)

main_txt = tkinter.Label(frame3, text="● 맞춤법 검사 기능은 믿을만한가요? "
                                      "\n▶ 네이버 맞춤법 검사기에 기반한 기술이지만 혹시 모르니 맹신하지 말고 참고용으로만 사용하는 것이 추천됩니다."
                                      "\n\n● 금기어 리스트 유의사항"
                                      "\n▶ 금기어에는 <기관명>, <상호명>, <국제기구> 등등의 카테고리가 있습니다."
                                      "\n모든 카테고리에 해당하는 금기어를 전부 리스트에 적을 수는 없기 때문에 학교생활기록부 작성 안내 종이를 꼭 참고하세요.", font=simple_font)
main_txt.pack(pady=10)

openimage_button=tkinter.Button(frame3, text="모든 금기어 사진 확인하기", command=open_banned_word_image)
openimage_button.pack(pady=10)

window.mainloop()