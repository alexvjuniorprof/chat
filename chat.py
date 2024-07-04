import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["chat_database"]
questions_collection = db["questions"]


def get_questions():
    return questions_collection.find({"index": {"$ne": None}}).sort(
        "index", pymongo.ASCENDING
    )


def main():
    questions_cursor = get_questions()

    questions = list(questions_cursor)

    if not questions:
        print("There are no questions.")

    for question in questions:
        question_text = question["question"]
        print(f"Pergunta: {question_text}")

        user_response = input("Sua resposta: ")
        print(f"Você respondeu: {user_response}")


if __name__ == "__main__":
    main()