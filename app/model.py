import pickle
from pyvi import ViTokenizer
import re


# Trước khi tiến hành dự đoán ta cần làm sạch dữ liệu và vec-tơ hóa dữ liệu văn bản
## Làm sạch dữ liệu
### Từ viết tắt
acronym_words = []
acronym_words_dict = []
acronym_words = open('acronym_word.txt','r', encoding='utf-8')
acronym_words = acronym_words.readlines()
for i in range(len(acronym_words)):
  acronym_words_split = acronym_words[i].split("\t")
  for j in range(len(acronym_words_split)):
    acronym_words_split[j] = re.sub("[\n\ufeff]",'',acronym_words_split[j])
  try:
    acronym_words_dict.append({acronym_words_split[0]:acronym_words_split[1]})
  except: 
    pass


# Từ dừng
stop_words = []
stop_words = open('stop_word.txt','r', encoding='utf-8')
stop_words = stop_words.readlines()
for i in range(len(stop_words)):
  stop_words[i] = re.sub("[\t\n\ufeff]",'',stop_words[i])


# Tách từ
def sementation(text):
  return ViTokenizer.tokenize(text)  # sử dụng thư viện vitokenizer để tách từ


# Chuẩn hóa unicode sang chuẩn unicode dựng sẵn
def loaddicchar():
    dic = {}
    char1252 = 'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ'.split(
        '|')
    charutf8 = "à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ".split(
        '|')
    for i in range(len(char1252)):
        dic[char1252[i]] = charutf8[i]
    return dic

dicchar = loaddicchar()
def covert_unicode(txt):
    return re.sub(
        r'à|á|ả|ã|ạ|ầ|ấ|ẩ|ẫ|ậ|ằ|ắ|ẳ|ẵ|ặ|è|é|ẻ|ẽ|ẹ|ề|ế|ể|ễ|ệ|ì|í|ỉ|ĩ|ị|ò|ó|ỏ|õ|ọ|ồ|ố|ổ|ỗ|ộ|ờ|ớ|ở|ỡ|ợ|ù|ú|ủ|ũ|ụ|ừ|ứ|ử|ữ|ự|ỳ|ý|ỷ|ỹ|ỵ|À|Á|Ả|Ã|Ạ|Ầ|Ấ|Ẩ|Ẫ|Ậ|Ằ|Ắ|Ẳ|Ẵ|Ặ|È|É|Ẻ|Ẽ|Ẹ|Ề|Ế|Ể|Ễ|Ệ|Ì|Í|Ỉ|Ĩ|Ị|Ò|Ó|Ỏ|Õ|Ọ|Ồ|Ố|Ổ|Ỗ|Ộ|Ờ|Ớ|Ở|Ỡ|Ợ|Ù|Ú|Ủ|Ũ|Ụ|Ừ|Ứ|Ử|Ữ|Ự|Ỳ|Ý|Ỷ|Ỹ|Ỵ',
        lambda x: dicchar[x.group()], txt)



# Xử dụng bộ từ điển để thay thế các kiểu gõ dấu và viết tắt
def replace_acronyms(text):
  text_list = text.split(" ");
  for i in range(len(text_list)):
    for j in range(len(acronym_words_dict)):
      key = list(acronym_words_dict[j].keys())[0]
      value = list(acronym_words_dict[j].values())[0]
      if text_list[i] == key:
        text_list[i] = value
  return " ".join(text_list)


# Xử lý các từ viết trùng lắp
def remove_loop_char(text):
  text = re.sub(r'([A-Z])\1+', lambda m: m.group(1).upper(), str(text), flags=re.IGNORECASE)
  text = re.sub(r'[^\s\wáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệóòỏõọôốồổỗộơớờởỡợíìỉĩịúùủũụưứừửữựýỳỷỹỵđ_]',' ',text)
  return text


# Loại bỏ stop word
def remove_stop_word(text):
  split_word = text.split(" ");
  words = []
  for word in split_word:
    if word not in stop_words:
      words.append(word)
  return " ".join(words)


  """**Tiền xử lý dữ liệu**"""
# Làm sạch dữ liệu
def text_prosessing(text):
  # Chuyển đổi thành chữ thường
  text = text.lower() 
  
  #Chuẩn hóa unicode sang chuẩn unicode dựng sẵn
  text = covert_unicode(text)

  # Xử dụng bộ từ điển để thay thế các kiểu gõ dấu và viết tắt
  text = replace_acronyms(text)

  # Xử lý các từ viết trùng lắp
  text = remove_loop_char(text)

  # # Xóa từ dừng
  # text = remove_stop_word(text)

  # Xóa các kí tự trong dấu []
  text = re.sub('\[.*?\]', '', text)

  # Xóa các kí tự đặc biệt
  text = re.sub("\W",' ',text) 

  # Xóa các đường link
  text = re.sub('https?://\S+|www\.\S+', ' ', text)

  # Xóa các số
  text = re.sub('\w*\d\w*', '', text)

  # Xóa các đoạn mã html
  text = re.sub(r'<[*>]*>',' ', text)

  #Xóa các kí tự xuống dòng
  text = " ".join(re.sub("\n", " ", text).split())

  # tách từ
  text = sementation(text)
  
  return text


# load không gian vector và model trờ lại từ file để dùng cho việc dự đoán
with open('CountVectorizerAndSVC.pkl', 'rb') as file:
  cv, model = pickle.load(file)


# Ta cần tải model từ file đã được lưu từ lúc huấn luyện
def predict(text):
    text = text_prosessing(text)  # tiền xử lý trước khi đưa vào mô hình để dự đoán
    X = [text]  # bao xung quanh string bằng 1 list để đưa vào vectorizer
    X_vector = cv.transform(X)
    y_pred = model.predict(X_vector)
    return y_pred[0]

# example
# result = predict('Gói cẩn thận, hàng chính hãng, rất thích, cảm ơn shop')
# print(result)
# result = predict('Hàng bị trầy xước')
# print(result)
