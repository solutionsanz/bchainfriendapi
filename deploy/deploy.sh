#!/bin/bash
#microservices..
  #bchainfriendapi..
  #git clone --quiet https://github.com/solutionsanz/bchainfriendapi >>/tmp/noise.out && cd bchainfriendapi
  kubectl create namespace bchainfriendapi >>/tmp/noise.out
  kubectl create -f kubernetes/bchainfriendapi-dpl.yaml >>/tmp/noise.out
  kubectl create -f kubernetes/bchainfriendapi-svc.yaml >>/tmp/noise.out
  kubectl create -f kubernetes/bchainfriendapi-ing.yaml >>/tmp/noise.out
