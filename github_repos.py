import requests
import pygal
import os
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS

#执行API调用并存储响应
language=''
while language != 'q':
    prompt='Please enter a programming language (Press q to quit)\n'
    language=input(prompt)
    if language =='q':
        exit()

    url = 'https://api.github.com/search/repositories?q=language:' \
          +language+'' \
          '&sort=stars'
    r = requests.get(url)

    if r.status_code!=200:
        print("Please input correctly and make sure Internet available ")
        continue
    print("Status code:", r.status_code)

    # Store API response in a variable.
    response_dict = r.json()
    print("Total repositories:", response_dict['total_count'])

    #探索有关仓库的信息
    repo_dicts=response_dict['items']

    names,plot_dicts=[],[]
    for repo_dict in repo_dicts:
        names.append(repo_dict['name'])

        if repo_dict['description'] is None:

            repo_dict['description']='No Data'

        plot_dict={
        'value':repo_dict['stargazers_count'],
        'label':repo_dict['description'],
        'xlink':repo_dict['html_url'],
            }
        plot_dicts.append(plot_dict)

    #可视化
    my_style=LS('#1122ff',base_style=LCS)

    my_config=pygal.Config()
    my_config.x_label_rotation=45
    my_config.show_legend=False   #隐藏图例
    my_config.truncate_label=15    #标签在15字符以内
    my_config.show_y_guides=False #隐藏水平线
    my_config.width=1000
    #my_config.y_labels_major_count=500 #不知道n有什么意义
    #my_config.y_labels_major_every=4   #将每n个y标签设为major
    #my_config.show_minor_y_labels=False

    chart=pygal.Bar(my_config,style=my_style)
    chart.title="Most-Starred " +language+ " Projects on Github"
    chart.x_labels=names

    chart.add('',plot_dicts)

    filename = language + '_repos.svg'
    chart.render_to_file(filename)

    os.startfile(filename)

