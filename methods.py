from imports import *


########################################################################################################################
def googleTrans(text, src, dest):
    print("text \n", text, "src \n", src, "dest \n", dest)

    try:
        translated_text = tr.google(text=text, from_language=src, to_language=dest)
        return translated_text
    except Exception as e:
        print("Google is Failed using another one\n", str(e))
        alter_trans = tr.youdao(text=text, from_language=src, to_language=dest)
        return alter_trans


def youdaoTrans(text, src, dest):
    print("text \n", text, "src \n", src, "dest \n", dest)

    try:
        translated_text = tr.youdao(text=text, from_language=src, to_language=dest)
        return translated_text
    except Exception as e:
        print("Youdao is Failed using another one\n", str(e))
        alter_trans = tr.google(text=text, from_language=src, to_language=dest)
        return alter_trans
########################################################################################################################


def findThematicsError(res):     # 11.285196244716644 11.285196244716644 11.285197734832764
    if res[0]["key"] == "Geography" and res[1]["key"] == "Technologies":
        if 11.285198 > res[0]["val"] > 11.285196:
            raise Exception("Neuron Net can`t extract any known tokens from text or text is too small. "
                            "Check if text is correctly in your query.")


def customTranslate(text, text_language, translate_to, translation_type):
    # if translation_type == 0:
        try:
            translated_text = googleTrans(text, text_language, translate_to)
            print(translated_text)

            return translated_text
        except Exception as e:
            print("TRANSLATION ERROR\n", str(e))

            return str(e)
    # else:
    #     try:
    #         translated_text = youdaoTrans(text, text_language, translate_to)
    #         print(translated_text)
    #
    #         return translated_text
    #     except Exception as e:
    #         print("TRANSLATION ERROR\n", str(e))
    #
    #         return str(e)


def translateToEnglish(text, translation_type):
    try:
        src = detect(text)
        if translation_type == 0:
            try:
                translated_text = googleTrans(text, src, 'en')
                print(translated_text)

                return translated_text
            except Exception as e:
                print("TRANSLATION ERROR\n", str(e))

                return str(e)
        else:
            try:
                translated_text = youdaoTrans(text, src, 'en')
                print(translated_text)

                return translated_text
            except Exception as e:
                print("TRANSLATION ERROR\n", str(e))

                return str(e)
    except Exception as e:
        print("ENGLISH TRANS IS FALL \n", e)


def identifyLang(text):  # func that detect a % of language in the text ( return a list )
    obj = obj_template
    res = list()

    lang_list = (detect_langs(text))

    for lang in lang_list:  # the list of strings
        template = dict()
        temp = dict(e.split(':') for e in str(lang).split(','))  # make a temp dictionary from the string

        for key in temp.keys():
            template['key'] = key
            template['val'] = float(temp[key])*100  # to percents %

        res.append(template)

    obj['res'] = res

    return obj


def identifyLangOffline(text):
    obj = obj_template
    res = list()
    template = dict()
    identifier = LanguageIdentifier.from_modelstring(langid_model, norm_probs=True)
    lang = identifier.classify(text)

    template['key'] = lang[0]
    template['val'] = float(lang[1]) * 100  # to percents %
    res.append(template)

    obj['res'] = res

    return obj


def splitAndTranslate(text, lang, translation_type):  # need to split str because Google API can not translate big texts
    default = 3
    lang_koef = language_val_dict.get(lang, default)  # influence to a text batch different to languages
    n = int(symbol_batch * lang_koef)  # n it is the size of split text parts

    try:
        split_text = list(map(''.join, zip(*[iter(text)] * n)))
        result_str = ""

        for sentence in split_text:
            result_str += translateToEnglish(sentence, translation_type)

        return result_str
    except:  # if batch to big to translate try again with smaller n
        n = symbol_batch*default
        split_text = list(map(''.join, zip(*[iter(text)] * n)))
        result_str = ""
        for sentence in split_text:
            result_str += translateToEnglish(sentence, translation_type)

        return result_str


def splitAndCustomTranslate(text, src, translation_type, dest):  # need to split str because Google API can not translate big texts
    default = 1
    lang_koef = 3  # influence to a text batch different to languages
    n = int(symbol_batch * lang_koef)  # n it is the size of split text parts

    try:
        split_text = list(map(''.join, zip(*[iter(text)] * n)))
        result_str = ""

        for sentence in split_text:
            result_str += customTranslate(sentence, src, dest, translation_type)

        return result_str
    except:  # if batch to big to translate try again with smaller n
        n = symbol_batch*default
        split_text = list(map(''.join, zip(*[iter(text)] * n)))
        result_str = ""
        for sentence in split_text:
            result_str += customTranslate(sentence, src, dest, translation_type)

        return result_str
