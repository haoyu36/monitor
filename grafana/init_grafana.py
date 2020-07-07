# -*- coding: utf-8 -*-


Key
eyJrIjoiaFlBR2dDTldwR3g1ZGIydE1KWDBDa2FSQkp5Z1VPRFoiLCJuIjoiYXBpaSIsImlkIjoxfQ==


curl -H "Authorization: Bearer eyJrIjoiaFlBR2dDTldwR3g1ZGIydE1KWDBDa2FSQkp5Z1VPRFoiLCJuIjoiYXBpaSIsImlkIjoxfQ==" 
http://127.0.0.1:3000/api/dashboards/home




# 创建数据源

/api/datasources


{
  "name":"zijin",
  "type":"prometheus",
  "url":"http://192.168.1.97:9090",
  "access":"proxy",
  "basicAuth":false
}




http://localhost:3000/api/dashboards/db

{
  "dashboard": json_file_content,
  "folderId": 0    # 保存仪表板的文件夹的ID
}





