import numpy as np
import pickle
import feature
import sklearn

def main(url): 
    status = []
    status.append(feature.having_ip_address(url))
    status.append(feature.abnormal_url(url))
    status.append(feature.count_dot(url))
    status.append(feature.count_www(url))
    status.append(feature.count_atrate(url))
    status.append(feature.no_of_dir(url))
    status.append(feature.no_of_embed(url))
    status.append(feature.shortening_service(url))
    status.append(feature.count_https(url))
    status.append(feature.count_http(url))
    status.append(feature.count_per(url))
    status.append(feature.count_ques(url))
    status.append(feature.count_hyphen(url))
    status.append(feature.count_equal(url))
    status.append(feature.url_length(url))
    status.append(feature.hostname_length(url))
    status.append(feature.suspicious_words(url))
    status.append(feature.digit_count(url))
    status.append(feature.letter_count(url))
    status.append(feature.fd_length(url))
    status.append(feature.tld_length(url))
    return status

def get_prediction_from_url(test_url):
    # Due to updates to scikit-learn, we now need a 2D array as a parameter to the predict function.
    features_test = main(test_url)
    features_test = np.array(features_test).reshape((1, -1))
    
    with open('random_forest_0966.pkl', 'rb') as f:
        rf = pickle.load(f)
    pred = rf.predict(features_test)
    if int(pred[0]) == 0:
        
        res="SAFE"
        return res
    elif int(pred[0]) == 1.0:
        
        res="DEFACEMENT"
        return res
    elif int(pred[0]) == 2.0:
        res="PHISHING"
        return res
        
    elif int(pred[0]) == 3.0:
        
        res="MALWARE"
        return res
    
urls = ['titaniumcorporate.co.za','en.wikipedia.org/wiki/North_Dakota']
for url in urls:
     print(get_prediction_from_url(url))