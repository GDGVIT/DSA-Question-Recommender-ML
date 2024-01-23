import numpy as np
import pandas as pd
import scipy
import joblib
from sklearn.preprocessing import RobustScaler
from flask import Flask, request, jsonify

mlapi=Flask(__name__)

@mlapi.route("/get_question/<int:cnt>",methods=["GET"])
def recommend_question(cnt):
    og_dat1=pd.read_csv(r"og_dataset.csv")
    prob_dat=pd.DataFrame(scipy.sparse.load_npz(r"prob_table.npz").toarray(),columns=pd.read_csv(r"prob_table_col_labels.csv",sep=',')['0'])
    prob_dat=prob_dat.sort_values(['Probability']).reset_index(drop=True)
    recomm=og_dat1[og_dat1['Cluster_label']==prob_dat.iloc[cnt,0]][['title','difficulty','related_topics']].to_json(orient='records')
    return jsonify(recomm), 200

@mlapi.route("/retrain")
def model_update(): # process time,update the clusters and update prob_table
    #loading tables
    og_dat=pd.read_csv(r"og_dataset.csv")
    user_time_label=pd.read_csv(r"user_time_taken_col_labels.csv",sep=',')
    time_dat=pd.DataFrame(scipy.sparse.load_npz(r"user_time_taken.npz").toarray(),columns=user_time_label['0'])
    user_prob_label=pd.read_csv(r"user_prob_table_col_labels.csv",sep=',')
    uprob_table=pd.DataFrame(scipy.sparse.load_npz(r"user_prob_table.npz").toarray(),columns=user_prob_label['0'])

    #processing time_taken feature

    #time_dat.loc[:,'time_taken']=time_dat.iloc[:,2:].mean(axis=1)
    og_dat.loc[:,'time_taken']=time_dat.iloc[:,2:].mean(axis=1)
    #time_dat=time_dat.loc[:,('id','Cluster_label','time_taken')]
    #user_time_label=user_time_label.iloc[:3,0]

    #retrain the model
    scaled_data=tran_mod.fit_transform(og_dat)
    mod.fit(scaled_data)

    #update the probability table
    og_dat['Cluster_label']=mod.labels_
    uprob_table['Cluster_label']=mod.labels_
    prob_table=uprob_table.iloc[:,1:].groupby(['Cluster_label']).sum()
    prob_table=prob_table.divide(uprob_table.iloc[:,:2].groupby(['Cluster_label']).count().loc[:,"id"],axis=0) #check
    prob_table=prob_table.mean(axis=1).round(5).abs().reset_index()
    prob_table.rename(columns={0:'Probability'},inplace=True)

    #saving all tables
    spar=scipy.sparse.csc_matrix(prob_table)
    scipy.sparse.save_npz(r"prob_table.npz",spar,True)
    spar2=scipy.sparse.csc_matrix(time_dat)
    scipy.sparse.save_npz(r"user_time_taken.npz",spar2,True)
    spar3=scipy.sparse.csc_matrix(uprob_table)
    scipy.sparse.save_npz(r"user_prob_table.npz",spar3,True)
    og_dat.to_csv(r"og_dataset.csv",sep=',')
    user_time_label.to_csv(r"user_time_taken_col_labels.csv",sep=',')
    user_prob_label.to_csv(r"user_prob_table_col_labels.csv",sep=',')

    return jsonify({"retrain_model":"success","message":"Model has been updated"})

@mlapi.route("/data_process_task/",methods=['POST'])
def table_update(): #replace time of og_dat after processing and add 'like' to og data
    data=request.get_json()
    og_dat3=pd.read_csv(r"og_dataset.csv")
    user_time_label=pd.read_csv(r"user_time_taken_col_labels.csv",sep=',')
    utime_dat=pd.DataFrame(scipy.sparse.load_npz(r"user_time_taken.npz").toarray(),columns=user_time_label['0'])
    user_prob_label=pd.read_csv(r"user_prob_table_col_labels.csv",sep=',')
    uprob_table=pd.DataFrame(scipy.sparse.load_npz(r"user_prob_table.npz").toarray(),columns=user_prob_label['0'])
    #print(data["user_id"],data["question_id"],data["liked"],data["time_taken"])
    if data["user_id"] not in user_time_label['0'].to_numpy():
        utime_dat[data["user_id"]]=0
        user_time_label=pd.DataFrame(np.append(user_time_label['0'],np.array([data["user_id"]]),axis=0)) #adding new user to time_table
    if data["user_id"] not in user_prob_label['0'].to_numpy():
        uprob_table[[data["user_id"]]]=0
        user_prob_label=pd.DataFrame(np.append(user_prob_label['0'],np.array([data["user_id"]]),axis=0))

    utime_dat.loc[(utime_dat['id']==data["question_id"],data["user_id"])]=data["time_taken"]
    og_dat3.loc[(og_dat3['id']==data["question_id"],'likes')]+=int(data["liked"]) # adding likes
    uprob_table.loc[(uprob_table['id']==data["question_id"],data["user_id"])]=1

    spar=scipy.sparse.csc_matrix(utime_dat)
    scipy.sparse.save_npz(r"user_time_taken.npz",spar,True)
    user_time_label.to_csv(r"user_time_taken_col_labels.csv",sep=',')

    spar1=scipy.sparse.csc_matrix(uprob_table)
    scipy.sparse.save_npz(r"user_prob_table.npz",spar1,True)
    user_prob_label.to_csv(r"user_prob_table_col_labels.csv",sep=',')
    og_dat3.to_csv(r"og_dataset.csv", sep=',', index=False)

    return jsonify({"success":"true","message":"All relevant files have been updated"}), 201

if __name__=='__main__':

    def process_func(x):
        scale_mod = RobustScaler(with_scaling=True, with_centering=True, unit_variance=False)
        dat = scale_mod.fit_transform(x)
        min_val = pd.DataFrame(dat).min()
        dat = pd.DataFrame(dat + np.array(min_val * -1))
        return dat
    mod = joblib.load(r"model.joblib")
    tran_mod = joblib.load(r"data_transformer.joblib")
    mlapi.run(debug=True)