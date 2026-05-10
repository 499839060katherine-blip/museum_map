# 中国乡村美术馆地图

## 项目结构

```
museum_map/
├── get_coordinates.py      # 获取坐标脚本
├── map.html               # 可视化地图页面
├── museums_data.json      # 博物馆坐标数据 (生成)
├── museums_with_coords.csv # CSV格式数据 (生成)
└── README.md              # 本文件
```

## 使用步骤

### 1. 获取高德地图 API Key

访问 [高德开放平台](https://lbs.amap.com/) 注册并申请 Web 服务 API Key。

### 2. 配置 API Key

```bash
export GAODE_API_KEY="你的API Key"
```

### 3. 运行坐标查询脚本

```bash
cd /Users/wang/museum_map
python3 get_coordinates.py
```

脚本会：
- 读取 Excel 文件中的 101 个美术馆数据
- 调用高德地图地理编码 API 获取每个地址的经纬度
- 保存为 `museums_with_coords.csv` 和 `museums_data.json`

### 4. 查看地图

1. 修改 `map.html` 中的高德地图 API Key:
   ```html
   <script src="https://webapi.amap.com/maps?v=2.0&key=你的API_Key"></script>
   ```

2. 在浏览器中打开 `map.html`

## 地图功能

- 📍 显示所有美术馆在地图上的位置
- 🔍 搜索功能（按名称、地址、省份筛选）
- 📊 统计信息（总数量、覆盖省份）
- 🖱️ 点击标记查看详情
- 📱 响应式设计

## 依赖

```bash
pip install pandas openpyxl requests
```

## 注意事项

- 高德地图 API 有免费调用额度限制
- 地理编码可能因地址精度问题返回空结果
- 建议在白天调用 API，响应更快
