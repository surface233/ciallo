import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import random as rd
import uuid  # 新增：生成唯一音频ID，避免冲突

# ========== 1. 初始化Session State（完全保留原逻辑） ==========
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "current_step1" not in st.session_state:
    st.session_state.current_step1 = 1
if "global_volume" not in st.session_state:
    st.session_state.global_volume = 0.5
if "fail" not in st.session_state:
    st.session_state.fail = 1

# ========== 2. 页面配置（完全保留原逻辑） ==========
st.set_page_config(
    page_title="丛雨摸头模拟器",
    page_icon="./image/murasame7.jpg",
)
st.title("丛雨摸头模拟器")

# ========== 3. 音量滑块（完全保留原逻辑） ==========
volume_slider = st.slider(
    "🎚️ 音量",
    min_value=0,
    max_value=100,
    value=int(st.session_state.global_volume * 100),
    step=5,
    key="volume_slider"
)
st.session_state.global_volume = volume_slider / 100
st.caption(f"当前音量：{volume_slider}%")

# ========== 4. 核心：按需转Base64 + 多音频播放JS框架 ==========
def sound_to_base64(sound_path):
    """按需读取音频文件并转成Base64"""
    if not os.path.exists(sound_path):
        st.warning(f"⚠️ 音效文件未找到：{sound_path}（可忽略，不影响游戏）")
        return ""
    with open(sound_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 初始化多音频播放的JS（只加载一次，支持叠加播放）
components.html("""
<script>
    // 存储所有活跃的音频实例（支持多音频同时播放）
    let audioInstances = {};

    // 播放音频（支持叠加，每个音频有唯一ID）
    window.parent.playAudioInstance = function(audioId, b64Data, volume) {
        // 创建新音频实例，不覆盖旧的
        const audio = new Audio(`data:audio/mp3;base64,${b64Data}`);
        audio.volume = volume;
        // 播放后记录实例，避免被垃圾回收
        audioInstances[audioId] = audio;
        // 播放完成后移除实例（可选，避免内存占用）
        audio.onended = function() {
            delete audioInstances[audioId];
        };
        // 播放音频（忽略浏览器自动播放限制的提示）
        audio.play().catch(err => {
            console.log("音效播放提示（浏览器限制）：", err);
        });
    };

    // 可选：暂停指定音频
    window.parent.pauseAudioInstance = function(audioId) {
        if (audioInstances[audioId]) {
            audioInstances[audioId].pause();
            audioInstances[audioId].currentTime = 0;
            delete audioInstances[audioId];
        }
    };

    // 可选：暂停所有音频
    window.parent.pauseAllAudio = function() {
        Object.keys(audioInstances).forEach(id => {
            audioInstances[id].pause();
            audioInstances[id].currentTime = 0;
        });
        audioInstances = {};
    };
</script>
""", height=0)

# ========== 5. 封装音频播放函数（支持叠加+自定义音量） ==========
def play_audio(audio_path, custom_volume=None):
    """
    播放指定音频（支持多音频叠加）
    :param audio_path: 音频文件路径
    :param custom_volume: 自定义音量（0-1），None则使用全局音量
    """
    b64_data = sound_to_base64(audio_path)
    if not b64_data:
        return
    # 生成唯一ID，确保多音频不冲突
    audio_unique_id = str(uuid.uuid4())
    # 优先使用自定义音量，否则用全局音量
    final_volume = custom_volume if custom_volume is not None else st.session_state.global_volume
    # 调用JS播放（支持叠加）
    components.html(f"""
    <script>
        window.parent.playAudioInstance("{audio_unique_id}", "{b64_data}", {final_volume});
    </script>
    """, height=0)

# 封装暂停所有音频的函数（可选，游戏结束时用）
def pause_all_audio():
    components.html("""
    <script>
        window.parent.pauseAllAudio();
    </script>
    """, height=0)

# ========== 6. 完整游戏逻辑（保留所有交互+支持多音频叠加） ==========
col1, _ = st.columns([5, 5])
with col1:
    if st.session_state.current_step1 == 1:
        st.markdown("开始游戏吗？<br>(关音菩萨提醒您，前方记得调小音量)", unsafe_allow_html=True)
        if st.button("《千恋万花》，启动！"):
            st.session_state.current_step1 = 2
            st.session_state.current_step = 1
            # song.mp3 固定10%音量（0.1），支持叠加
            play_audio("./audio/song.mp3", custom_volume=0.1)
            st.rerun()

# 步骤1：初始选择
if st.session_state.current_step == 1:
    if st.session_state.fail == 2:
        # song.mp3 固定10%音量
        play_audio("./audio/song.mp3", custom_volume=0.1)
        st.session_state.fail = 1
    st.image("./image/murasame9.jpg", width=300, caption="狗修金又在看奇怪的网站了！")
    st.write("这是一个丛雨，要摸头吗")
    if st.button("👋摸摸头"):
        st.session_state.current_step = 2.1
        st.rerun()
    elif st.button("不要!!!"):
        st.session_state.current_step = 2.2
        st.rerun()

# 步骤2.1：摸头分支（Murasame1.mp3 用全局音量，可叠加）
elif st.session_state.current_step == 2.1 :
    st.image("./image/murasame5.webp", width=300, caption="狗修金？")
    play_audio("./audio/Murasame1.mp3")
    if st.button("继续摸"):
        st.session_state.current_step = 3
        st.rerun()
    elif st.button("不摸了,寸止"):
        st.session_state.current_step = 2.2
        st.rerun()

# 步骤2.2：拒绝摸头分支（Murasame2.mp3 用全局音量，可叠加）
elif st.session_state.current_step == 2.2:
    st.image("./image/murasame2.jpg", width=300, caption="狗！修！金！！！")
    play_audio("./audio/Murasame2.mp3")
    if st.button("吓我一跳,释放时间回溯忍术！"):
        st.session_state.current_step = 1
        st.rerun()
    elif st.button("被幼刀吓哭了，那只能摸了😭😭😭"):
        st.session_state.current_step = 2.1
        st.rerun()
    elif st.button("不、不摸...那咋啦？"):
        st.session_state.current_step = -1
        st.rerun()

# 步骤3：继续摸头分支（Murasame3.mp3 用全局音量，可叠加）
elif st.session_state.current_step == 3:
    st.image("./image/murasame3.jpg", width=300, caption="狗~修~金~💗")
    play_audio("./audio/Murasame3.mp3")
    if st.button("无线摸头摸个爽！"):
        st.session_state.current_step = 2.1
        st.rerun()
    elif st.button("不摸了,她总不能是滑动变阻器吧"):
        st.session_state.current_step = 2.2
        st.rerun()

# 步骤-1：游戏结束分支（Murasame4.mp3 + man.mp3 同时播放，叠加）
elif st.session_state.current_step == -1:
    # 先暂停之前的音频（可选，避免杂音）
    pause_all_audio()
    # 两个音频同时播放（叠加），都用全局音量
    play_audio("./audio/Murasame4.mp3")
    play_audio("./audio/man.mp3")
    st.markdown("丛雨吃掉了你的手指！<br>游戏结束！", unsafe_allow_html=True)
    st.image("./image/murasame4.webp", width=300, caption="豪赤😋！！！")
    if st.button("第三炸弹，败者食尘！"):
        # 暂停结束音效，播放song.mp3（10%音量）
        pause_all_audio()
        play_audio("./audio/song.mp3", custom_volume=0.1)
        st.session_state.current_step = 1
        st.session_state.fail = 2
        st.rerun()

# ========== 7. Ciallo彩蛋按钮（随机音效，支持叠加） ==========
st.image("./image/ciallo.jpg", width=300, caption="雑魚柚子厨~💗💗💗")
if st.button("点击Ciallo~ (∠・ω< )⌒★"):
    num = rd.randint(1, 6)
    play_audio(f"./audio/ciallo{num}.mp3")