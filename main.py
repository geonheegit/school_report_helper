from hanspell import spell_checker
import tkinter.ttk
import tkinter.font
import re

window=tkinter.Tk()

window.title("생기부 도우미 by 30313 한건희")
window.geometry("1040x640+50+50")
window.resizable(True, True)

# 생기부 금지어 리스트
forbidden_words = []

# 폰트
bold_font=tkinter.font.Font(family="맑은 고딕", size=20, slant="roman")
sub_font=tkinter.font.Font(family="맑은 고딕", size=15, slant="roman")

# 버튼 함수
def count():
    linespace_count = 0
    count_txt = count_textbox.get("1.0", tkinter.END)
    for i in count_txt:
        if "\n" in i:
            linespace_count += 1
    counted_number = len(str(count_txt)) - 1
    txt_bytes = len(str(count_txt).encode()) - 1 + linespace_count
    count_result_txt.config(text=f'▶ {txt_bytes}바이트, 공백 포함 {counted_number}자')
    print(linespace_count)

def check_spell():
    enter_removed_original_txt = ""

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
    for i in no_empty_new_str:
        splitted_result = spell_checker.check(i.encode("utf-8"))
        errors += splitted_result.errors
        checked_splitted_list.append(splitted_result.checked)

        for k, v in splitted_result.words.items():
            if v != 0:
                joined_str += str(k)
                joined_str += ", "

        if "<end>" in joined_str:
            joined_str = re.sub('<end>', '', joined_str)
        if "<br>" in joined_str:
            joined_str = re.sub('<br>', '', joined_str)
        if "&quot;" in joined_str:
            joined_str = re.sub('&quot;', '', joined_str)

    # print(checked_splitted_list)

    summed_str = ""
    for i in checked_splitted_list:
        summed_str += str(i)
    # print(summed_str)

    # result = spell_checker.check(summed_str.encode("utf-8"))
    entry_fixed_txt.delete("1.0", tkinter.END)
    entry_fixed_txt.insert("1.0", summed_str)

    changed_number_txt.config(text = f'▶ 수정한 사항: {errors}개')

    spell_error_txt.insert("1.0", joined_str)


# 창 분할
notebook=tkinter.ttk.Notebook(window, width=1040, height=600)
notebook.pack()

# 1번 창 생성
frame1_1=tkinter.Frame(window)
notebook.add(frame1_1, text="맞춤법 검사")

# 1번 창 구성 요소들
title_txt=tkinter.Label(frame1_1, text="맞춤법 검사기", font=bold_font)
title_txt.pack(pady=10)

input_txt=tkinter.Label(frame1_1, text="▼ 검사할 내용 입력 ▼")
input_txt.pack(pady=10)

entry_before_check = tkinter.Text(frame1_1, width=100, height=10, spacing2=5)
entry_before_check.pack(pady=20)
entry_before_check.insert(tkinter.END, "검사할 내용을 입력하세요.")

changed_number_txt=tkinter.Label(frame1_1, text="▶ 수정한 사항: ")
changed_number_txt.pack(pady=5)

spell_error_txt=tkinter.Text(frame1_1, width=100, height=4, spacing2=5)
spell_error_txt.pack(pady=10)

entry_fixed_txt = tkinter.Text(frame1_1, width=100, height=10, spacing2=5)
entry_fixed_txt.pack(pady=20)
entry_fixed_txt.insert(tkinter.END, "검사 결과")

check_button=tkinter.Button(frame1_1, text="검사하기", command=check_spell)
check_button.pack(pady=10)

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
                                            "▶행동특성및종합의견: 1500바이트, 약 500자")
count_result_txt.pack(pady=5)

count_textbox = tkinter.Text(frame2, width=100, height=25, spacing2=5)
count_textbox.pack(pady=20)
count_textbox.insert(tkinter.END, "내용을 입력하세요.")

count_button=tkinter.Button(frame2, text="검사하기", command=count)
count_button.pack(pady=10)

count_result_txt=tkinter.Label(frame2, text="▶ 바이트, 자", font = sub_font)
count_result_txt.pack(pady=5)

window.mainloop()