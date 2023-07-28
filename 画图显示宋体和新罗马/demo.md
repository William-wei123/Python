'
from matplotlib.font_manager import FontProperties
from matplotlib import rcParams
from matplotlib import pyplot
import matplotlib.pyplot as plt

# 设置中文字体为SimSun（宋体）
font_prop = FontProperties(fname="C:\Windows\Fonts/SimSun.ttc")
font_legend_prop = FontProperties(fname="C:\Windows\Fonts/SimSun.ttc", size=14)
# 设置英文标签为Times New Roman字体
english_font = FontProperties(fname="C:\Windows\Fonts/times.ttf")
# 混合字体设置，
config = {
#     "font.family":'serif',
#     "font.size": 80,
       "mathtext.fontset":'stix',
#     "font.serif": ['SimSun'],
}
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
rcParams.update(config)


# 设置横轴标签
plt.xlabel('经度($\mathrm{Lot}$)',fontproperties=font_prop)

# 设置横轴标签
plt.ylabel('纬度($\mathrm{Lat}$)',fontproperties=font_prop)
plt.xticks(fontproperties=english_font)
plt.yticks(fontproperties=english_font)

name_list.append('observe')
name_list.append('true')
# Visualization2map2(List_lat_lot, os.path.dirname(path), f'test', name_list)
pyplot.title('船舶$\mathrm{1}$', fontproperties=font_prop)
# pyplot.legend()
# 将label设置不同的字体
labelss = plt.legend(prop = {'size':14}).get_texts()
[label.set_fontname('Times New Roman') for label in labelss]
label = labelss[-1]
label.set_fontproperties(font_legend_prop)
# label = labelss[-2]
# label.set_fontproperties(font_prop)
# 设置刻度线在坐标轴内侧
pyplot.tick_params(axis='both', direction='in')

# pyplot.show()
pyplot.savefig(os.path.dirname(path)+f'/test{min_index}.png', dpi=300, bbox_inches='tight')
'
