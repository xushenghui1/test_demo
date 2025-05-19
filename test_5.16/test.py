def read_residue_mapping(pdb_file):
    """读取PDB文件中的残基序号和氨基酸类型的映射"""
    residue_info = []
    current_res = None
    with open(pdb_file, 'r') as f:
        for line in f:
            if line.startswith('ATOM '):
                res_num = int(line[22:26].strip())
                res_name = line[17:20].strip()
                if current_res != res_num:
                    residue_info.append((res_num, res_name))
                    current_res = res_num
    return residue_info

def process_pdb(input_pdb, reference_pdb, output_pdb):
    """根据参考PDB文件的残基编号重新编号输入的PDB文件"""
    # 获取两个文件的残基信息
    ref_residues = read_residue_mapping(reference_pdb)
    model_residues = read_residue_mapping(input_pdb)
    
    # 确保残基数量相同
    if len(ref_residues) != len(model_residues):
        print(f"警告：残基数量不匹配！参考：{len(ref_residues)}，模型：{len(model_residues)}")
        return
    
    # 创建残基编号映射
    residue_mapping = {}
    for (model_num, model_res), (ref_num, ref_res) in zip(model_residues, ref_residues):
        if model_res != ref_res:
            print(f"警告：残基类型不匹配！位置 {model_num}: {model_res} != {ref_res}")
            return
        residue_mapping[model_num] = ref_num
    
    # 重新编号并写入新文件
    with open(input_pdb, 'r') as f_in, open(output_pdb, 'w') as f_out:
        for line in f_in:
            if line.startswith('ATOM '):
                old_num = int(line[22:26].strip())
                new_num = residue_mapping[old_num]
                # 替换残基编号
                new_line = f"{line[:22]}{new_num:4d}{line[26:]}"
                f_out.write(new_line)
            elif line.startswith(('TER', 'END')):
                f_out.write(line)

if __name__ == "__main__":
    # 文件路径
    original_pdb = "7xen.pdb"        # 原始PDB文件
    model_pdb = "7xen-1.pdb"         # 需要处理的PDB文件
    output_pdb = "7xen-1_renumbered.pdb"  # 输出文件
    
    # 处理PDB文件
    process_pdb(model_pdb, original_pdb, output_pdb)
    print("处理完成！输出文件已保存为:", output_pdb)
