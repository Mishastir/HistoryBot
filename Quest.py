class Quests:

    def __init__(self, question_number=0):
        self.question_number = question_number
        self.number_of_tries = 0
        self.started = False
        self.question = []
        self.answer = []
        self.hint = []
        self.way = []
        self.quest_list = ""
        self.go_forward = False

    def start_quest(self, items):
        quest_list = list(items)
        self.quest_list = quest_list
        k = 0
        for peace in quest_list:
            if k % 4 == 0:
                self.question.append(peace)
            elif k % 4 == 1:
                self.answer.append(peace)
            elif k % 4 == 2:
                self.hint.append(peace)
            elif k % 4 == 3:
                self.way.append(peace)
            k += 1

    def answers_handler(self, answer, way, hint, question_number, text, quest_list):
        one_of_answers = answer[question_number].split(",")
        check = False
        number_of_tries = self.number_of_tries
        text = text.strip()
        for peace in one_of_answers:
            peace = peace.strip()
            if text.lower() == peace.lower():
                check = True
                break
            elif text.lower() != peace.lower():
                check = False
        if check:
                self.question_number += 1
                self.number_of_tries = 0
                if self.question_number > len(quest_list) / 4:
                    self.question_number = 0
                    return "Вітаємо, на цьому ваш квест завершено"
                else:
                    self.go_forward = True
                    return "Ваша відповідь вірна. " + way[self.question_number-1]
        else:
            self.go_forward = False
            if number_of_tries < 2 or number_of_tries > 3:
                self.number_of_tries += 1
                return "Спробуйте ще"
            elif number_of_tries == 2:
                self.number_of_tries += 1
                return 0
            elif number_of_tries == 3:
                self.number_of_tries += 1
                if text == "Так":
                    return hint[self.question_number]
                elif text == "Ні":
                    return "Добре, продовжуйте вгадувати"

    def main(self, items, text):
        self.start_quest(items)

        return self.pre_answers_handler(text)

    def pre_answers_handler(self, text):
        question_number = self.question_number
        if self.question_number <= len(self.quest_list) / 4 - 1 and text != "/endquest":
            return self.answers_handler(self.answer, self.way, self.hint, self.question_number, text, self.quest_list)
        elif self.question_number == len(self.quest_list) / 4:
            self.question_number = 0
            self.started = False
            return """На цьому ваш квест завершено, дякуюємо за те, що прийняли участь.
                            Ваш результат: """ + str(question_number)
        elif text == "/endquest":
            self.question_number = 0
            self.started = False
            return "Ви закінчили квест із результатом " + str(question_number)

    def next_question(self, items, text):
        self.start_quest(items)
        if self.question_number <= len(self.quest_list) / 4 - 1 and text != "/endQuest":
            return "Ваше наступне питання: \n" + self.question[self.question_number]
        else:
            return 0
