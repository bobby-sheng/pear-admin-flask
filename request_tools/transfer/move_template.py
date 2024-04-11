#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import jsonpath
from .filelog import logger
from .login import Login
from .common import ensure_path_sep, get_yaml_data

Config = get_yaml_data(ensure_path_sep("\\transfer\\config.yaml"))


class Template(Login):

    @staticmethod
    def data_treating(res_data, env, request_session):
        """
        处理获取的版本数据，需要的信息存入字典
        :param request_session:
        :param env:
        :param res_data:
        :return:
        """
        url = f"http://{Config.get(env)['host']}{Config.get('type_list_api')}"
        type_list_res = request_session.get(url).json()
        assert type_list_res["code"] == 200, "dst环境型号列表请求失败"
        data_dict = {}
        for item in res_data['data']['list']:
            key = item['id']
            tpye_id = item['typeId']
            jsonpath_rule = f'$.data.list[?(@.id=="{tpye_id}")].deviceType'
            data_dict[key] = {
                'name': item['name'],
                'vendorName': item['vendorName'],
                'workingType': item['workingType'],
                'typeName': item['typeName'],
                'deviceType': jsonpath.jsonpath(type_list_res, jsonpath_rule)[0]
            }
        return data_dict

    def get_src_template_info(self):
        """
        请求源环境版本列表api，处理返回值
        :return:
        """
        url = f"http://{Config.get('src')['host']}{Config.get('version_list_api')}"
        data = {"sorts": {}, "filters": {}}
        res = self.src_session.post(url, json=data).json()
        assert res["code"] == 200, "源环境登录失败，请检查账号密码是否正常"
        logger.info("======获取src模版信息成功======")
        str_output = self.data_treating(res, 'src', self.src_session)
        return str_output

    def get_dst_template_info(self):
        """
        请求源环境版本列表api，处理返回值
        :return:
        """
        url = f"http://{Config.get('dst')['host']}{Config.get('version_list_api')}"
        data = {"sorts": {}, "filters": {}}
        res = self.dst_session.post(url, json=data).json()
        assert res["code"] == 200, "目的环境登录失败，请检查账号密码是否正常"
        logger.info("======获取dst模版信息成功======")
        dst_output = self.data_treating(res, 'dst', self.dst_session)
        return dst_output

    def src_template_exist_or_not(self):
        """
        判断源环境模版配置在目环境中是否存在，如存在则绑定至对应字典中。依赖dst_id标识等待后续的新建覆盖动作
        :return:
        """
        str_output = self.get_src_template_info()
        dst_output = self.get_dst_template_info()
        for s, r in str_output.items():
            for d, t in dst_output.items():
                if r == t:
                    r['dst_id'] = d
        logger.info("checking：检查src，dst环境模版之间的差异！")
        return str_output

    @staticmethod
    def get_version_api(request_session, env, version_id):
        """
        获取目的地址的版本id与解析模版、下发模版id的关联与替换
        :return:
        """
        url_path = str(Config.get('version_template_info')).replace("version_id", version_id)
        url = f"http://{Config.get(env)['host']}{url_path}"
        res = request_session.get(url).json()
        assert res["code"] == 200, "获取版本详情接口报错"

        return res

    def write_template_api(self, write_data: list):
        """
        获取目的地址的版本id与解析模版、下发模版id的关联与替换
        :return:
        """
        url = f"http://{Config.get('dst')['host']}{Config.get('write_template_api')}"
        res = self.dst_session.put(url, json=write_data).json()
        assert res["code"] == 200, "写入报错"
        return res

    def add_version_template(self, version_data):
        """
        判断厂商是否存在，不存在则新增。新增厂商、型号、版本
        :return:
        """
        # version_data = {'name': '12', 'vendorName': 'Huawei', 'workingType': 'CLI', 'typeName': 'CE12800',
        #                 'deviceType': 'sky_switch_router'}

        logger.info("======开始新增==========")
        vendor_res_id = ""
        type_res_id = ""
        version_res_id = ""
        # 新增厂商
        vendor_url = f"http://{Config.get('dst')['host']}{Config.get('add_vendor')}"
        vendor_data = {"icon": "icon-firewall-default", "name": version_data["vendorName"]}
        vendor_res = self.dst_session.post(vendor_url, json=vendor_data).json()

        if 200 == vendor_res['code']:
            vendor_res_id = jsonpath.jsonpath(vendor_res, "$.data.id")[0]
        elif "already exists" in vendor_res['message']:
            get_vendor_list_url = f"http://{Config.get('dst')['host']}{Config.get('vendor_list_api')}"
            get_vendor_list_res = self.dst_session.get(get_vendor_list_url).json()
            json_vendor_list = f'$.data.list[?(@.name=="{version_data["vendorName"]}")].id'
            vendor_res_id = jsonpath.jsonpath(get_vendor_list_res, json_vendor_list)[0]
        else:
            logger.info(f"新建{version_data['vendorName']}失败，并且在dst环境中也无法找到此厂商，请检查！！")
        logger.info(f"厂商id：{vendor_res_id}")

        # 新增型号
        type_url = f"http://{Config.get('dst')['host']}{Config.get('add_type')}"
        type_data = {"vendorId": vendor_res_id, "name": version_data["typeName"],
                     "deviceType": version_data["deviceType"]}

        type_res = self.dst_session.post(type_url, json=type_data).json()

        if 200 == type_res['code']:
            type_res_id = jsonpath.jsonpath(type_res, "$.data.id")[0]

        elif "already exists" in type_res['message']:
            get_type_list_url = f"http://{Config.get('dst')['host']}{Config.get('type_list_api')}"
            get_type_list_res = self.dst_session.get(get_type_list_url).json()
            json_type_list = f'$.data.list[?(@.name=="{version_data["typeName"]}")].id'
            type_res_id = jsonpath.jsonpath(get_type_list_res, json_type_list)[0]
        else:
            logger.info(f"新建{version_data['vendorName']}失败，并且在dst环境中也无法找到此型号，请检查！！")
        logger.info(f"型号id：{type_res_id}")

        # 新增版本
        version_url = f"http://{Config.get('dst')['host']}{Config.get('add_version')}"
        version_data = {"typeId": type_res_id, "name": version_data["name"],
                        "workingType": version_data["workingType"]}

        version_res = self.dst_session.post(version_url, json=version_data).json()
        if 200 == version_res['code']:
            version_res_id = jsonpath.jsonpath(version_res, "$.data.id")[0]
        elif "already exists" in version_res['message']:
            get_version_list_url = f"http://{Config.get('dst')['host']}{Config.get('version_list_api')}"
            get_version_list_data = {"sorts": {}, "filters": {}}
            get_version_list_res = self.dst_session.post(get_version_list_url, json=get_version_list_data).json()
            json_version_list = f'$.data.list[?(@.name=="{version_data["name"]}")].id'
            version_res_id = jsonpath.jsonpath(get_version_list_res, json_version_list)[0]
        else:
            logger.info(f"新建{version_data['name']}失败，并且在dst环境中也无法找到此版本，请检查！！")
        logger.info(f"版本id：{version_res_id}")

        dst_version_info = self.get_version_api(self.dst_session, 'dst', version_res_id)
        # 获取dst的version解析、下发模版id
        dst_command_template_id = jsonpath.jsonpath(dst_version_info, "$.data.commandTemplate..id")[0]
        dst_parse_template_id = jsonpath.jsonpath(dst_version_info, "$.data.parseTemplate..id")[0]
        logger.info("======新增完成======")

        return dst_command_template_id, dst_parse_template_id, version_res_id

    def read_write_template(self):
        """
        读取写入模版，目的地址存在版本就覆盖，不存在就重新新增
        :return:
        """
        str_output = self.src_template_exist_or_not()
        logger.info("start：检查模版是否存在dst环境，如果存在就进行覆盖，不存在就进行新增模版同步数据")
        for k, v in str_output.items():
            src_version_data = self.get_version_api(self.src_session, 'src', k)

            # 获取src的version解析、下发模版参数
            src_command_template_data = jsonpath.jsonpath(src_version_data, "$.data.commandTemplate")[0]
            src_parse_template_data = jsonpath.jsonpath(src_version_data, "$.data.parseTemplate")[0]

            if "dst_id" in v:
                log_data = {'vendorName': v['vendorName'], 'typeName': v['typeName'], 'versionName': v['name'], }
                dst_version_info = self.get_version_api(self.dst_session, 'dst', v['dst_id'])

                # 获取dst的version解析、下发模版id
                dst_command_template_id = jsonpath.jsonpath(dst_version_info, "$.data.commandTemplate..id")[0]
                dst_parse_template_id = jsonpath.jsonpath(dst_version_info, "$.data.parseTemplate..id")[0]

                # 修改src获取的模版id为dst的解析、下发模版id作为接口参数
                src_command_template_data[0]["id"] = dst_command_template_id
                src_parse_template_data[0]["id"] = dst_parse_template_id
                res_write = self.write_template_api([src_command_template_data[0], src_parse_template_data[0]])
                assert res_write["code"] == 200, "上传接口失败,查看日志检查两个环境模版情况！"
                logger.info(f"覆盖成功！{log_data}")
            else:
                dst_command_template_id, dst_parse_template_id, version_res_id = self.add_version_template(v)
                v['dst_id'] = version_res_id
                src_command_template_data[0]["id"] = dst_command_template_id
                src_parse_template_data[0]["id"] = dst_parse_template_id
                res_write = self.write_template_api([src_command_template_data[0], src_parse_template_data[0]])
                assert res_write["code"] == 200, "上传接口失败,查看日志检查两个环境模版情况！"
                logger.info(f"同步成功！{v} ")
        logger.info("end：模版同步全部完成！！")
        return str_output


if __name__ == '__main__':
    logger.info(Template().read_write_template())
