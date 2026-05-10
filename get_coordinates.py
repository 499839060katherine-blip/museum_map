import pandas as pd
import requests
import json
import time
import os

# 高德地图 API Key - 请替换为你的 Key
GAODE_API_KEY = os.environ.get('GAODE_API_KEY', 'YOUR_API_KEY_HERE')

def get_location(address, name):
    """使用高德地图地理编码 API 获取坐标"""
    url = "https://restapi.amap.com/v3/geocode/geo"

    # 优化地址，添加省份信息提高准确率
    full_address = address
    if not address.startswith('中国') and not address.startswith('浙江省') \
       and not address.startswith('江苏省') and not address.startswith('安徽省'):
        # 尝试补充省份
        for province in ['浙江', '江苏', '安徽', '福建', '江西', '山东',
                        '河南', '湖北', '湖南', '广东', '四川', '贵州',
                        '云南', '陕西', '甘肃', '青海', '台湾']:
            if address.startswith(province):
                break

    params = {
        'key': GAODE_API_KEY,
        'address': full_address,
        'output': 'JSON'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        if data.get('status') == '1' and data.get('geocodes'):
            location = data['geocodes'][0]['location']
            lng, lat = location.split(',')
            return {
                'longitude': float(lng),
                'latitude': float(lat),
                'formatted_address': data['geocodes'][0].get('formatted_address', '')
            }
        else:
            print(f"  ⚠️  未找到坐标: {name} - {address}")
            return None
    except Exception as e:
        print(f"  ❌ 查询失败: {name} - {e}")
        return None

def main():
    # 读取Excel
    file_path = "/Users/wang/Downloads/副本国内乡村美术馆(1) 2.xlsx"
    df = pd.read_excel(file_path)

    # 清理数据
    df = df[['序号', '省份', '美术馆名称', '地址', '概况']].dropna(subset=['美术馆名称', '地址'])

    print(f"共 {len(df)} 个美术馆需要查询坐标")
    print("="*50)

    results = []

    for idx, row in df.iterrows():
        name = row['美术馆名称']
        address = row['地址']
        province = row['省份']
        overview = str(row['概况'])[:100] if pd.notna(row['概况']) else ''

        print(f"[{idx+1}/{len(df)}] 查询: {name}")

        location = get_location(address, name)

        if location:
            results.append({
                'name': name,
                'province': province,
                'address': address,
                'longitude': location['longitude'],
                'latitude': location['latitude'],
                'overview': overview
            })
            print(f"  ✓ 坐标: {location['longitude']}, {location['latitude']}")
        else:
            results.append({
                'name': name,
                'province': province,
                'address': address,
                'longitude': None,
                'latitude': None,
                'overview': overview
            })

        # API 调用间隔，避免频率限制
        time.sleep(0.2)

    # 保存结果
    result_df = pd.DataFrame(results)
    result_df.to_csv('/Users/wang/museum_map/museums_with_coords.csv', index=False, encoding='utf-8-sig')

    # 生成统计
    success_count = result_df['longitude'].notna().sum()
    print("\n" + "="*50)
    print(f"查询完成: {success_count}/{len(results)} 个成功获取坐标")
    print(f"结果已保存到: /Users/wang/museum_map/museums_with_coords.csv")

    # 保存为JSON供地图使用
    valid_results = [r for r in results if r['longitude'] is not None]
    with open('/Users/wang/museum_map/museums_data.json', 'w', encoding='utf-8') as f:
        json.dump(valid_results, f, ensure_ascii=False, indent=2)

    print(f"地图数据已保存到: /Users/wang/museum_map/museums_data.json")

if __name__ == '__main__':
    main()
