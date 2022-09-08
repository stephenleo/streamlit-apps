🌟 View code on [Github](https://github.com/stephenleo/streamlit-apps/blob/main/pages/01_%F0%9F%8E%93_Graduate_School_Admissions.py)

✍️ Read the blog post on [Medium](https://towardsdatascience.com/boy-or-girl-a-machine-learning-web-app-to-detect-gender-from-name-16dc0331716c?sk=16897adf79bfe50ec7cf61ad3c1a0f37)

This is a Machine Learning web app to detect gender from name. Find out a name’s likely gender using Natural Language Processing character embedding and an LSTMs model.

1. **How does it work?**
    - "Boy or Girl?" uses a Machine Learning algorithm called "LSTM" to read a name and output whether the name is a boy's name or a girl's name.
    - The algorithm has learnt how to make these output predictions by learning from over 35,000 English first names.
    - The training dataset is from the [USA_NAMES](https://console.cloud.google.com/marketplace/product/social-security-administration/us-names) Big Query open dataset
2. **Does it work for non-English names?**
    - The algorithm was developed by feeding it English names and hence it has the highest accuracy on English names. However, I did notice decent accuracy on Indian names since they share the same root language. The accuracy seems to be bad on Chinese or non-English sounding names.
3. **Do you store my information?**
    - No. The algorithm runs on the names your provide and plots out the output predictions. The names are lost after that and the app does not store any information.