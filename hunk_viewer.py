import streamlit as st
import pickle

def increment_index(maxindex):
    if st.session_state.cveindex+1<=maxindex:
        st.session_state.cveindex+=1
    else:
        st.balloons()
        st.toast("You're done!", icon="🎉")
def write_ans(ans,reason,maxindex):
    with open("annotation.txt","a+") as f:
        f.write(str(st.session_state.cveindex)+","+ans+","+"\""+reason.replace("\"","").replace("\n","")+"\""+"\n")
        increment_index(maxindex)
def jump_index(jumpnum,maxindex):
    if jumpnum<=maxindex:
        st.session_state.cveindex=jumpnum
    else:
        st.toast("Index you are trying to jump to does not exist :(")
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

test = "test"
st.download_button('Download test', test, 'text/csv')
maxindex = len(cve)-1
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
    #st.title("Index/Primary key (starts from ZERO): "+str(st.session_state.cveindex))
    st.title("Hunk viewer for annotators")
    st.title(cve[st.session_state.cveindex])
    st.markdown("Description: "+desc[st.session_state.cveindex])
    st.code(hunks[st.session_state.cveindex])
    ans = st.radio("Is it relevant?", ["yes", "no"])
    reason = st.text_input("Reasoning if no","Type here")
    st.button("Submit",on_click=write_ans, args=(ans,reason,maxindex,))