FROM python:2
WORKDIR /myApp
ADD . /myApp
RUN pip install flask jsonify pprint requests flask_restful
EXPOSE 5000
CMD python BChainFriendAPI.py 
