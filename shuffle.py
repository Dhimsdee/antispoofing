import random

def question_bank(index):
    questions = [
                "smile",
                "surprise",
                "blink eyes",
                "angry",
                "turn face right",
                "turn face left"]
    return questions[index]

limit_questions = 6

num = list(range(0,limit_questions))
random.shuffle(num)
print(num)

for i in num:
    question = question_bank(i)
    print(question)