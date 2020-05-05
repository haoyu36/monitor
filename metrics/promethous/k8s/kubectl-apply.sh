#!/bin/bash


kubectl apply -f setup
kubectl apply -f node-exporter
kubectl apply -f kube-state-metrics
kubectl apply -f prometheus
kubectl apply -f grafana
kubectl apply -f alertmanager


