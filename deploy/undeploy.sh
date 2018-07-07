#!/bin/bash
#microservices..
  #bchainfriendapi..
  kubectl delete -f deploy/kubernetes/bchainfriendapi-ing.yaml >>/tmp/noise.out
  kubectl delete -f deploy/kubernetes/bchainfriendapi-svc.yaml >>/tmp/noise.out
  kubectl delete -f deploy/kubernetes/bchainfriendapi-dpl.yaml >>/tmp/noise.out
  kubectl delete namespace bchainfriendapi >>/tmp/noise.out