def question_bank(index):
    questions = [
                "Senyum",
                "Terkejut",
                "Kedipkan Mata",
                "Marah",
                "Putar Wajah ke Kanan",
                "Putar Wajah ke Kiri"]
    return questions[index]

def challenge_result(question, out_model,blinks_up):
    if question == "Senyum":
        if len(out_model["emotion"]) == 0:
            challenge = "fail"
        elif out_model["emotion"][0] == "happy": 
            challenge = "pass"
        else:
            challenge = "fail"
    
    elif question == "Terkejut":
        if len(out_model["emotion"]) == 0:
            challenge = "fail"
        elif out_model["emotion"][0] == "surprise": 
            challenge = "pass"
        else:
            challenge = "fail"

    elif question == "Marah":
        if len(out_model["emotion"]) == 0:
            challenge = "fail"
        elif out_model["emotion"][0] == "angry": 
            challenge = "pass"
        else:
            challenge = "fail"

    elif question == "Putar Wajah ke Kanan":
        if len(out_model["orientation"]) == 0:
            challenge = "fail"
        elif out_model["orientation"][0] == "right": 
            challenge = "pass"
        else:
            challenge = "fail"

    elif question == "Putar Wajah ke Kiri":
        if len(out_model["orientation"]) == 0:
            challenge = "fail"
        elif out_model["orientation"][0] == "left": 
            challenge = "pass"
        else:
            challenge = "fail"

    elif question == "Kedipkan Mata":
        if blinks_up == 1: 
            challenge = "pass"
        else:
            challenge = "fail"

    return challenge