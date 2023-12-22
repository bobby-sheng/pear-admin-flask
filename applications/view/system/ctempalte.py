from flask import Blueprint, render_template, request
import pandas as pd

from applications.common.utils.rights import authorize


bp = Blueprint('ctempalte', __name__, url_prefix='/ctempalte')


# app = Flask(__name__)
# PER_PAGE = 10
@bp.route('/', methods=['GET', 'POST'])
@authorize("system:ctempalte:main")
def index():
    if request.method == 'POST':
        # Get the uploaded files
        file1 = request.files['file1']
        file2 = request.files['file2']

        # Save the files to disk
        file1.save('file1.xlsx')
        file2.save('file2.xlsx')

        # Compare the files
        differences = compare_excel('file1.xlsx', 'file2.xlsx')

        # Render the template with the differences

        return render_template('system/ctempalte/result.html', differences=differences)

    return render_template('system/ctempalte/upload.html')

    # Function to compare Excel files

@bp.get('/')
@authorize("system:ctempalte:main")
def main():
    if request.method == 'POST':
        # Get the uploaded files
        file1 = request.files['file1']
        file2 = request.files['file2']

        # Save the files to disk
        file1.save('file1.xlsx')
        file2.save('file2.xlsx')

        # Compare the files
        differences = compare_excel('file1.xlsx', 'file2.xlsx')

        # Render the template with the differences

        return render_template('system/ctempalte/upload.html', differences=differences)

    return render_template('system/ctempalte/result.html')

    # Function to compare Excel files


def compare_excel(file1, file2):
    # Read the two Excel files
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Get the '名称' column from both files
    names1 = df1['名称']
    names2 = df2['名称']
    differences = []
    if len(names1) != len(names2):
        # Get the names that are unique to each file
        unique_names1 = names1[~names1.isin(names2)]
        unique_names2 = names2[~names2.isin(names1)]

        # Add the unique names to the differences list
        for name in unique_names1:
            if name == "预定义服务对象":
                break
            differences.append({"不同原因": "名称不同", "名称": name, "文件1": name, "文件2": "文件2没有这个模版内容！！"})
        for name in unique_names2:
            if name == "预定义服务对象":
                break
            differences.append({"不同原因": "名称不同", "名称": name, "文件1": "文件1没有这个模版内容！！", "文件2": name})
    # Find the common names
    common_names = names1[names1.isin(names2)]

    # Initialize a list to store the differences

    # Iterate over the common names
    for name in common_names:
        # Get the data rows for the corresponding name in both files
        data1 = df1[df1['名称'] == name].iloc[0]
        data2 = df2[df2['名称'] == name].iloc[0]
        if name == "预定义服务对象":
            break
        if data1['名称'] != data2['名称']:
            differences.append({"不同原因": "名称不同", "名称": name, "文件1": "none", "文件2": "none"})
        # Compare the '类型', '键', and '模板' fields
        if data1['类型'] != data2['类型']:
            # differences.append(f"类型不同：名称={name}, 文件1={data1['类型']}..., 文件2={data2['类型']}...")
            differences.append({"不同原因": "类型不同", "名称": name, "文件1": data1['类型'], "文件2": data2['类型'], })
        if data1['键'] != data2['键']:
            # differences.append(f"键不同：名称={name}, 文件1={data1['键']}..., 文件2={data2['键']}...")
            differences.append({"不同原因": "键不同", "名称": name, "文件1": data1['键'], "文件2": data2['键'], })

        if data1['模板'] != data2['模板']:
            differences.append({"不同原因": "模板不同", "名称": name, "文件1": data1['模板'], "文件2": data2['模板'], })
            # differences.append(f"模板不同：名称={name}, 文件1={data1['模板']}..., 文件2={data2['模板']}...")

    # Return the differences

    return differences