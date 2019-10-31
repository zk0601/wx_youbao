# 小区价格影响因素接口
## 如果查询的小区不存在，返回的数据中就不包含此小区

### URL: private/card/get_comm_price_factor

### Method: GET

### Parameters
| name | type | description | required |
| ----- | ----- | ----- | ----- |
| comm_ids | string | 小区id列表（"comm_id1,comm_id2,comm_id3"） | 是 |

### Response

#### payload
| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| comm_price_list | array | 小区价格列表 |

#### payload
| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| id | int | 小区id |
| comm_price_factor_dict | array | 小区价格因素列表 |

#### payload.price_list.comm_price_factor_dict
| 字段名 | 类型 | 描述 |
| --- | --- | --- |
| comm_id | int | 小区id |
| city_centre_distance | int | 距离市中心距离(米) |
| build_year | int | 建筑年代 |
| green_rate | float | 绿化率 |
| volume_rate | float | 容积率 |


```json
{
    "encrypt": 0,
    "err_code": "10000",
    "err_msg": "成功",
    "data": {
        "payload": [
            {
                "comm_id": 2467,
                "city_centre_distance": 7997,
                "build_year": 1999,
                "green_rate": 0.28,
                "volume_rate": 4,
                "comm_price": 51639
            },
            {
                "comm_id": 2468,
                "city_centre_distance": 16048,
                "build_year": 2015,
                "green_rate": 0.45,
                "volume_rate": 0.8,
                "comm_price": 39847
            }
        ]
    }
}
```


### Errors

* `10002` 参数错误
* `10007` 签名错误
