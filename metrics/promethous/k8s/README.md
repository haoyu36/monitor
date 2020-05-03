

部署使用的 yaml 文件来自于 coreos/kube-prometheus


```shell
# 初始化文件
bash init.sh

# 开始部署
bash kubectl-apply.sh

# 配置 ingress
kubectl apply -f ingress.yml
```


- [coreos/kube-prometheus](https://github.com/coreos/kube-prometheus)





# istio


- [How to collect istio metrics using prometheus operator](https://github.com/coreos/prometheus-operator/issues/2502)





