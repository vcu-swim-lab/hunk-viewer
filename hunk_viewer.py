import streamlit as st
import pickle
import time

def increment_index(maxindex):
    if st.session_state.cveindex+1<=maxindex:
        st.session_state.cveindex+=1
        st.experimental_rerun()
    else:
        st.balloons()
        st.toast("You're done!", icon="🎉")
def write_ans(cve_to_index,ans,reasons,maxindex):
    with open("annotation.txt","a+") as f:
        i=0
        for a in range(len(ans)):    
            f.write(cve_to_index[st.session_state.cveindex]+","+str(i)+","+ans[a]+","+"\""+reasons[a].replace("\"","").replace("\n","")+"\""+"\n")
            i+=1
        increment_index(maxindex)
def jump_index(jumpnum,maxindex):
    if jumpnum<=maxindex:
        st.session_state.cveindex=jumpnum
#        st.experimental_rerun()
    else:
        st.toast("Index you are trying to jump to does not exist :(")
        time.sleep(1)
hunks = []
with open("dumps/hunks_array.pkl","rb") as f:
    hunks = pickle.load(f)
hunk_nos = []
with open("dumps/hunk_nos_array.pkl","rb") as f:
    hunk_nos = pickle.load(f)
desc = []
with open("dumps/desc_array.pkl","rb") as f:
    desc = pickle.load(f)
cve = []
with open("dumps/cve_array.pkl","rb") as f:
    cve = pickle.load(f)
cve_to_index = []
thing = [cve_to_index.append(c) for c in cve if c not in cve_to_index]
maxindex = len(cve_to_index)-1
print(maxindex)
if "cveindex" not in st.session_state:
    st.session_state.cveindex = 0
page = st.empty()
with open("annotation.txt") as f:
    st.download_button("Download CSV",f)
with st.expander("Jump to..."):
    st.markdown("Current Index/Primary key (starts from ZERO): "+str(st.session_state.cveindex))
    jumpnum = st.text_input("Jump to what index","0")
    button2 = st.button("Jump now!",on_click=jump_index,args=(int(jumpnum),maxindex,))
with page.container():

    with st.form("my form"):
        #st.title("Index/Primary key (starts from ZERO): "+str(st.session_state.cveindex))
        st.title("Hunk viewer for annotators")
        st.title(cve_to_index[st.session_state.cveindex])
        indices = []
        for i in range(len(cve)):
            if cve[i]==cve_to_index[st.session_state.cveindex]:
                indices.append(i)
        st.markdown("Description: "+desc[indices[0]])
        ans = []
        reasons = []
        for i in indices:
            st.markdown("Hunk "+str(i))
            st.code(hunks[i])
            ans.append(st.radio("Is it relevant?", ["yes", "no"], key=i))
            reasons.append(st.text_input("Reasoning if no","Type here", key=10000-i))
        submitted = st.form_submit_button("Submit")#,on_click=write_ans, args=(cve_to_index,ans,reasons,maxindex,))
        if submitted:
            write_ans(cve_to_index,ans,reasons,maxindex)