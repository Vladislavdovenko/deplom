from imports import *
from methods import *

app = Flask(__name__)
random.seed(version=2)


@app.route("/")  # will show this info at the main page of localhost
def main():
    return \
        '<h2>This is an API service</h2>' \
        '<h3>Guide for using</h3>' \
        '<div>Try POST on <b> /thematics </b> to detect thematic of web-site </div>' \
        '<div>The JSON in POST must be {text:"your text"}</div>' \
        '<div>In /thematics JSON in POST must be {text:"your text", limit:INT}</div>' \
        '<br>'


@app.route("/slow", methods=['POST'])  # to test multi-threading
def slow():
    start_time = time.time()
    time.sleep(14)

    timing = time.time() - start_time
    message = {'_time': timing, 'err': None, 'res': None, 'text': "Zz-zz-zz"}

    return jsonify(message)


@app.route("/language", methods=['POST'])
def sendLangMessage():
    global emergency, text, start_time
    start_time = time.time()
    emergency = False

    try:
        json = request.get_json()  # get data
        text = str(json['text'])
        version = json.get('version', False) or 'default'

        if version == 'google':
            message = identifyLang(text)
        elif version == 'langid':
            message = identifyLangOffline(text)
        else:
            emergency = True
            message = identifyLang(text)
            emergency = True

        timing = time.time() - start_time
        message['_time'] = timing
    except Exception as e:
        if emergency:
            message = identifyLangOffline(text)
            timing = time.time() - start_time
            message['_time'] = timing

            return jsonify(message)

        message_err = {'_time': None, 'err': str(e), 'res': None}
        timing = time.time() - start_time
        message_err['_time'] = timing

        return jsonify(message_err)

    return jsonify(message)


@app.route("/translate", methods=['POST'])
def sendTranslatedMessage():
    start_time = time.time()
    try:
        json = request.get_json()  # get data
        text = str(json['text'])

        message = {'_time': None, 'err': None, 'res': translateToEnglish(text, random.random())}

        timing = time.time() - start_time
        message['_time'] = timing

        return message
    except Exception as e:
        message_err = {'_time': None, 'err': str(e), 'res': None}
        timing = time.time() - start_time
        message_err['_time'] = timing

        return jsonify(message_err)


@app.route("/custom/translate", methods=['POST'])
def sendCustomTranslatedMessage():
    start_time = time.time()
    time.sleep(random.randint(3, 5))
    try:
        json = request.get_json()  # get data
        text = str(json['text'])
        text_language = str(json['src'])
        translate_to = str(json['dest'])

        message = {'_time': None, 'err': None, 'res': splitAndCustomTranslate(text, text_language, 0, translate_to)}

        timing = time.time() - start_time
        message['_time'] = timing
    except Exception as e:
        message_err = {'_time': None, 'err': str(e), 'res': None}
        timing = time.time() - start_time
        message_err['_time'] = timing

        return jsonify(message_err)

    return jsonify(message)


@app.route("/thematics", methods=['POST'])  # will send a JSON by the POST query
def addMessage():
    start_time = time.time()
    global graph, words_limit

    with graph.as_default():
        try:
            json = request.get_json()  # get data

            text = str(json['text'])
            limit = int(json['limit'])

            if limit == 0:  # set limit if nothing get
                limit = words_limit

            text = re.sub("^\s+|\n|\r|\s+$", ' ', text)  # to delete trash like \n or \r

            text_len = len(text)
            words_in_text = len(text.split())

            if words_in_text < limit:  # if parsing was bad return nothing
                return jsonify(
                    {'_time': 0,
                     'err': "Text not parsed correctly. Try to increase limit.",
                     'res': []}
                )

            lang = detect(text)
            print(lang)

            if lang == 'en':  # if text in English don`t need any translation
                token = tokenizer.texts_to_matrix([text], mode='binary')
                print("ENGLISH \n", text)
            else:
                if text_len > symbol_batch:  # for big text we need to split it into smaller parts
                    text_to_check = splitAndTranslate(text, lang, random.random())
                else:  # small text we can translate as a one part
                    text_to_check = translateToEnglish(text, random.random())

                token = tokenizer.texts_to_matrix([text_to_check], mode='binary')
                print(text_to_check)

            token = np.array(token)
            prediction = model.predict(token)
            message = makeObj(prediction[0])

            findThematicsError(message['res'])

            timing = time.time() - start_time
            message['_time'] = timing

            return jsonify(message)
        except Exception as e:
            message_err = {'_time': None, 'err': str(e), 'res': None}

            timing = time.time() - start_time
            message_err['_time'] = timing

            return jsonify(message_err)


if __name__ == "__main__":
    app.run(
        threaded=True,
        host=host, port=port
    )
