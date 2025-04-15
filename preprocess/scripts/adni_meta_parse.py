import pandas as pd
import os
import csv
import random
random.seed(10)

INPUT_PATH1 = "/Users/zhangyi/Downloads/ADNI_converted_2010_2012"
INPUT_PATH2 = "/Users/zhangyi/Downloads/ADNI_converted3"
INPUT_PATH3 = "/Users/zhangyi/Downloads/ADNI_converted_ad"
INPUT_PATH4 = "/Users/zhangyi/Downloads/ADNI_converted"
INPUT_PATH5 = "/Users/zhangyi/Downloads/ADNI_converted_ad2"
INPUT_PATH6 = "/Users/zhangyi/Downloads/ADNI_converted_mci"

ALL_META_PATH = "/Users/zhangyi/Downloads/ADNI_converted_meta_all"
# The merged meta file and split tsv files will be under /Users/zhangyi/Downloads/ADNI_converted_meta_all/
# The merged image data will be under /Users/zhangyi/Downloads/ADNI_converted_2010_2012/

FILE_NAME = "participants.tsv"


def image_cnt_per_subject(input_path):
    # Get image counts for each subject in converted outputs
    pid_list = []
    count = []
    for p in os.listdir(input_path):
        if "sub-ADNI" in p:
            # print(p)
            pid_list.append(p)
            count.append(len(os.listdir(os.path.join(input_path, p))))
    df = pd.DataFrame({
        "participant_id": pid_list,
        "image_count": count
    })
    return df


def get_participants_meta(input_path):
    df = pd.read_csv(os.path.join(input_path, FILE_NAME), sep='\t')
    df["diagnosis_sc"] = df["diagnosis_sc"].apply(lambda x: "MCI" if x in ["EMCI", "LMCI"] else x)  
    return df


def session_level(input_path):
    # Get image counts for each subject in converted outputs
    pid_list = []
    session_list = []
    # count = []
    for p in os.listdir(input_path):
        if "sub-ADNI" in p:
            for s in os.listdir(os.path.join(input_path, p)):
                pid_list.append(p)
                session_list.append(s)
    df = pd.DataFrame({
        "participant_id": pid_list,
        "session_id": session_list
    })
    return df


def merge_converted_data(source_path, dest_path):
    df_src = get_participants_meta(source_path)
    df_src = df_src[df_src["diagnosis_sc"].isin(["AD", "MCI", "CN"])]
    for subject in df_src["participant_id"]:
        subject = str(subject).strip()
        if os.path.exists(os.path.join(dest_path, subject)):
            cmd = f"cp -r {os.path.join(source_path, subject, "*")} {os.path.join(dest_path, subject)}"
        else:
            cmd = f"cp -r {os.path.join(source_path, subject)} {dest_path}"
        print(cmd)
        # TODO:
        os.system(cmd)


def merge_converted_meta_all(output_path):
    df1 = get_participants_meta(INPUT_PATH1)
    df2 = get_participants_meta(INPUT_PATH2)
    df3 = get_participants_meta(INPUT_PATH3)
    df4 = get_participants_meta(INPUT_PATH4)
    df5 = get_participants_meta(INPUT_PATH5)
    df6 = get_participants_meta(INPUT_PATH6)
    
    df_union = pd.concat([df1, df2, df3, df4, df5, df6])
    df_union = df_union[df_union["diagnosis_sc"].isin(["AD", "MCI", "CN"])]
    df_union = df_union.drop_duplicates(["participant_id"])
    df_union.to_csv(output_path, sep='\t', index=False, quoting=csv.QUOTE_NONE)


def generate_split_tsv(input_path, output_path):
    # pid_list = []
    session_list = []
    # count = []
    for p in os.listdir(input_path):
        if "sub-ADNI" in p:
            for s in os.listdir(os.path.join(input_path, p)):
                # pid_list.append(p)
                session_list.append((p, s))
    random.shuffle(session_list)
    total_length = len(session_list)
    split1 = int(total_length * 0.7)
    split2 = split1 + int(total_length * 0.15)
    
    # Split the list into three parts
    train = session_list[:split1]
    val = session_list[split1:split2]
    test = session_list[split2:]
    df_train = pd.DataFrame(train, columns=["participant_id", "session_id"])
    df_train.to_csv(os.path.join(output_path, "Train_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)

    df_val = pd.DataFrame(val, columns=["participant_id", "session_id"])
    df_val.to_csv(os.path.join(output_path, "Val_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)

    df_test = pd.DataFrame(test, columns=["participant_id", "session_id"])
    df_test.to_csv(os.path.join(output_path, "Test_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)
    # generate split data with diagnosis data
    df_par = get_participants_meta(output_path) 
    df_train_diag = add_diagnosis_info(df_train, df_par)
    df_train_diag.to_csv(os.path.join(output_path, "Train_diagnosis_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)
    df_val_diag = add_diagnosis_info(df_val, df_par)
    df_val_diag.to_csv(os.path.join(output_path, "Val_diagnosis_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)
    df_test_diag = add_diagnosis_info(df_test, df_par)
    df_test_diag.to_csv(os.path.join(output_path, "Test_diagnosis_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)


def add_diagnosis_info(df_split, df_par):
    df = pd.merge(df_split, df_par, on="participant_id", how="inner")
    df["diagnosis"] = df["diagnosis_sc"]
    df["mmse"] = df["mmse_bl"]
    df["cdr"] = df["apoe_gen1"]
    df["cdr_sb"] = df["apoe_gen2"]
    age = df["session_id"].str.split("M").str[-1].astype(int) / 12 + df["age_bl"].astype(float)
    df["age"] = age
    df["examination_date"] = "2007-03-01"
    df["earliest_time"] = "2007-03-01"
    df["age_rounded"] = round(age, 1)
    df = df[["participant_id", "session_id", "diagnosis", "mmse", "cdr", "cdr_sb", "age", "examination_date", "earliest_time", "age_rounded"]]
    return df


def merge_image_data():
    # Merge image data and meta tsv data
    merge_converted_data(INPUT_PATH2, INPUT_PATH1)
    merge_converted_data(INPUT_PATH3, INPUT_PATH1)
    merge_converted_data(INPUT_PATH4, INPUT_PATH1)
    merge_converted_data(INPUT_PATH5, INPUT_PATH1)
    merge_converted_data(INPUT_PATH6, INPUT_PATH1)


def merge_meta_all():
    merge_converted_meta_all("/Users/zhangyi/Downloads/ADNI_converted_meta_all/participants.tsv")


def generate_split_all():
    # Generate tsv files for data preprocess split and also include diagnosis info
    generate_split_tsv(INPUT_PATH1, ALL_META_PATH)


def sample_tsv(n):
    df = pd.read_csv(os.path.join(ALL_META_PATH, "Train_ADNI.tsv"), sep='\t')
    df = df.head(int(n * 0.7))
    df.to_csv(os.path.join(ALL_META_PATH, f"sample_{n}/Train_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)
    df = pd.read_csv(os.path.join(ALL_META_PATH, "Train_diagnosis_ADNI.tsv"), sep='\t')
    df = df.head(int(n * 0.7))
    df['age_rounded'] = (df['age_rounded'] * 2).round() / 2
    df.to_csv(os.path.join(ALL_META_PATH, f"sample_{n}/Train_diagnosis_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)

    df = pd.read_csv(os.path.join(ALL_META_PATH, "Val_ADNI.tsv"), sep='\t')
    df = df.head(int(n * 0.15))
    df.to_csv(os.path.join(ALL_META_PATH, f"sample_{n}/Val_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)
    df = pd.read_csv(os.path.join(ALL_META_PATH, "Val_diagnosis_ADNI.tsv"), sep='\t')
    df = df.head(int(n * 0.15))
    df['age_rounded'] = (df['age_rounded'] * 2).round() / 2
    df.to_csv(os.path.join(ALL_META_PATH, f"sample_{n}/Val_diagnosis_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)

    df = pd.read_csv(os.path.join(ALL_META_PATH, "Test_ADNI.tsv"), sep='\t')
    df = df.head(int(n * 0.15))
    df.to_csv(os.path.join(ALL_META_PATH, f"sample_{n}/Test_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)
    df = pd.read_csv(os.path.join(ALL_META_PATH, "Test_diagnosis_ADNI.tsv"), sep='\t')
    df = df.head(int(n * 0.15))
    df['age_rounded'] = (df['age_rounded'] * 2).round() / 2
    df.to_csv(os.path.join(ALL_META_PATH, f"sample_{n}/Test_diagnosis_ADNI.tsv"), sep='\t', index=False, quoting=csv.QUOTE_NONE)


def image_count_by_group():
    # Image count
    df1 = get_participants_meta(ALL_META_PATH)
    df_ic = image_cnt_per_subject(INPUT_PATH1)
    df_merged1 = pd.merge(df1, df_ic, on="participant_id", how="inner")
    label_count = df_merged1.groupby(["diagnosis_sc"])["image_count"].sum()
    print(label_count)

# image_count_by_group()
# Output
# AD      897
# CN     1112
# MCI    1074

sample_tsv(200)

# df_ic = image_cnt_per_subject(INPUT_PATH1)
# # print(df_ic)
# df1 = get_participants_meta(INPUT_PATH1)

# df_ic2 = image_cnt_per_subject(INPUT_PATH2)
# # print(df_ic)
# df2 = get_participants_meta(INPUT_PATH2)

# # print(pd.merge(df1, df2, on="participant_id", how="inner"))
# # Check any session overlap between two downloads
# df_sec1 = session_level(INPUT_PATH1)
# df_sec2 = session_level(INPUT_PATH2)
# # print(df_sec1)
# # print(df_sec2)
# print(pd.merge(df_sec1, df_sec2, on=["participant_id", "session_id"], how="inner"))

# # union multiple participant tsv files and drop duplicate
# df_union = pd.concat([df1, df2])
# df_union = df_union.drop_duplicates(["participant_id"])
# print(df1["participant_id"].count())
# print(df2["participant_id"].count())
# # drop_duplicates()
# print(df_union["participant_id"].count())

# # Image count
# df_merged1 = pd.merge(df1, df_ic, on="participant_id", how="inner")

# label_count = df_merged1.groupby(["diagnosis_sc"])["image_count"].sum()

# df_merged2 = pd.merge(df2, df_ic2, on="participant_id", how="inner")

# label_count2 = df_merged1.groupby(["diagnosis_sc"])["image_count"].sum()

# Generate tsv files
# data split


