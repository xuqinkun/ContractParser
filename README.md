# 合同解析
## Usage
python main.py input_dir output_dir \
ps:
    input_dir: json文件根目录
    output_dir：输出Excel保存目录
# 备注：
整体输出格式如下：
文件夹一级名称，如“01.陶加海外”
文件夹末级名称，如“001.Delta Industrial Ceramica SA”
文件名称，如“Annual Contract(DELTA)”
输出共3个excel，上述3个字段+“单品合同字段”；上述3个字段+“整线合同字段”；上述3个字段+“国外合同字段”；
备注：暂定以为含有“销售奖励制度”的为单品合同，在文件夹《02陶加国内》、文件夹《02陶加国内》文件夹内的文档读取，含有“约定单价”的为整线合同，剩余的为“其他”；在文件夹《01.陶加海外》、文件夹《03.石加海外》的为国外合同

