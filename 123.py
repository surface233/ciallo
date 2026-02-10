import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import random as rd

# ========== 1. 全局配置：提前定义常量（避免重复赋值） ==========
# 音频/图片路径常量（集中管理，便于维护）
AUDIO_PATHS = {
    "song": "./audio/song.mp3",
    "Murasame1": "./audio/Murasame1.mp3",
    "Murasame2": "./audio/Murasame2.mp3",
    "Murasame3": "./audio/Murasame3.mp3",
    "Murasame4": "./audio/Murasame4.mp3",
    "ciallo1": "./audio/ciallo1.mp3",
    "ciallo2": "./audio/ciallo2.mp3",
    "ciallo3": "./audio/ciallo3.mp3",
    "ciallo4": "./audio/ciallo4.mp3",
    "ciallo5": "./audio/ciallo5.mp3",
    "ciallo6": "./audio/ciallo6.mp3",
    "man": "./audio/man.mp3"
}

IMAGE_PATHS = {
    "icon": "./image/murasame7.jpg",
    "m9": "./image/murasame9.jpg",
    "m5": "./image/murasame5.webp",
    "m2": "./image/murasame2.jpg",
    "m3": "./image/murasame3.jpg",
    "m4": "./image/murasame4.webp",
    "ciallo": "./image/ciallo.jpg"
}

# ========== 2. 缓存核心耗时函数（最关键优化） ==========
# 缓存音频Base64转换：仅首次加载/文件变化时执行
@st.cache_resource(ttl=None, show_spinner="加载音效文件中...")
def sound_to_base64_cached(sound_path):
    """缓存版音频转Base64，避免每次交互重复读取文件"""
    if not os.path.exists(sound_path):
        st.error(f"😥 音效文件找不到！路径：{sound_path}")
        return ""
    with open(sound_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 缓存图片加载（部署后加速图片渲染）
@st.cache_resource(ttl=None)
def load_image_cached(img_path):
    """缓存图片路径，避免重复读取"""
    if not os.path.exists(img_path):
        st.error(f"😥 图片文件找不到！路径：{img_path}")
        return None
    return img_path

# ========== 3. 初始化Session State（顺序不变，精简写法） ==========
DEFAULT_STATE = {
    "current_step": 0,
    "current_step1": 1,
    "global_volume": 0.5,
    "fail": 1
}
for key, val in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ========== 4. 页面配置（提前加载图标缓存） ==========
st.set_page_config(
    page_title="丛雨摸头模拟器",
    page_icon=load_image_cached(IMAGE_PATHS["icon"]),
)
st.title("丛雨摸头模拟器")

# ========== 5. 音量滑块（逻辑不变，精简变量） ==========
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

# ========== 6. 预加载所有音频Base64（缓存后仅执行一次） ==========
sound_base64_map = {
    key: sound_to_base64_cached(path) for key, path in AUDIO_PATHS.items()
}
# 生成音频src（按原ID映射）
sound_src = f"data:audio/mp3;base64,{sound_base64_map['song']}"
sound_src1 = f"data:audio/mp3;base64,{sound_base64_map['Murasame1']}"
sound_src2 = f"data:audio/mp3;base64,{sound_base64_map['Murasame2']}"
sound_src3 = f"data:audio/mp3;base64,{sound_base64_map['Murasame3']}"
sound_src4 = f"data:audio/mp3;base64,{sound_base64_map['Murasame4']}"
sound_src5 = f"data:audio/mp3;base64,{sound_base64_map['ciallo1']}"
sound_src6 = f"data:audio/mp3;base64,{sound_base64_map['ciallo2']}"
sound_src7 = f"data:audio/mp3;base64,{sound_base64_map['ciallo3']}"
sound_src8 = f"data:audio/mp3;base64,{sound_base64_map['ciallo4']}"
sound_src9 = f"data:audio/mp3;base64,{sound_base64_map['ciallo5']}"
sound_src10 = f"data:audio/mp3;base64,{sound_base64_map['ciallo6']}"
sound_src11 = f"data:audio/mp3;base64,{sound_base64_map['man']}"

# ========== 7. 核心音频HTML组件（缓存+精简标签+修复JS） ==========
@st.cache_resource(ttl=None)
def render_audio_html(global_volume):
    """缓存音频HTML/JS，仅音量变化时重新渲染（避免每次重跑都生成）"""
    return f"""
<audio id="sound-effect" style="display: none;">
    <source src="{sound_src}" type="audio/mp3">
</audio>
<audio id="sound-effect1" style="display: none;">
    <source src="{sound_src1}" type="audio/mp3">
</audio>
<audio id="sound-effect2" style="display: none;">
    <source src="{sound_src2}" type="audio/mp3">
</audio>
<audio id="sound-effect3" style="display: none;">
    <source src="{sound_src3}" type="audio/mp3">
</audio>
<audio id="sound-effect4" style="display: none;">
    <source src="{sound_src4}" type="audio/mp3">
</audio>
<audio id="sound-effect5" style="display: none;">
    <source src="{sound_src5}" type="audio/mp3">
</audio>
<audio id="sound-effect6" style="display: none;">
    <source src="{sound_src6}" type="audio/mp3">
</audio>
<audio id="sound-effect7" style="display: none;">
    <source src="{sound_src7}" type="audio/mp3">
</audio>
<audio id="sound-effect8" style="display: none;">
    <source src="{sound_src8}" type="audio/mp3">
</audio>
<audio id="sound-effect9" style="display: none;">
    <source src="{sound_src9}" type="audio/mp3">
</audio>
<audio id="sound-effect10" style="display: none;">
    <source src="{sound_src10}" type="audio/mp3">
</audio>
<audio id="sound-effect11" style="display: none;">
    <source src="{sound_src11}" type="audio/mp3">
</audio>
<script>
    // 修复：新增所有音频ID，确保音量同步
    const ALL_AUDIO_IDS = [
        'sound-effect','sound-effect1','sound-effect2','sound-effect3','sound-effect4',
        'sound-effect5','sound-effect6','sound-effect7','sound-effect8','sound-effect9',
        'sound-effect10','sound-effect11'
    ];

    // 通用函数：更新所有音频的整体音量
    function updateGlobalVolume(volume) {{
        ALL_AUDIO_IDS.forEach(audioId => {{
            const audio = document.getElementById(audioId);
            if (audio) audio.volume = volume;
        }});
        console.log(`✅ 整体音量已更新为：${{volume*100}}%`);
    }}

    // 初始化音量
    updateGlobalVolume({global_volume});

    // 通用音量设置函数
    function setAudioVolume(audioId, volume) {{
        const audio = document.getElementById(audioId);
        if (audio) audio.volume = volume;
        console.log(`✅ ${{audioId}} 音量设为：${{volume*100}}%`);
    }}

    // 核心音效函数（逻辑完全不变）
    window.parent.playSound = function() {{
        const audio = document.getElementById('sound-effect');
        audio.currentTime = 0;
        setAudioVolume('sound-effect', 0.1*{global_volume});
        audio.play().catch(err => {{
            alert("😥 启动音效播放失败，请检查音频权限～");
        }});
    }};

    window.parent.Pause = function(audioId, resetPosition = true) {{
        const audio = document.getElementById(audioId);
        if (!audio) return;
        if (audio.paused) return;
        audio.pause();
        if (resetPosition) audio.currentTime = 0;
        console.log(`✅ 已暂停指定音频：${{audioId}}`);
    }};

    window.parent.playSound1 = function() {{
        const audio = document.getElementById('sound-effect1');
        audio.currentTime = 0;
        setAudioVolume('sound-effect1', 1.0 * {global_volume});
        window.parent.Pause('sound-effect2');
        window.parent.Pause('sound-effect3');
        window.parent.Pause('sound-effect4');
        audio.play().catch(err => {{
            alert("😥 启动音效播放失败，请检查音频权限～");
        }});
    }};

    window.parent.playSound2 = function() {{
        const audio = document.getElementById('sound-effect2');
        audio.currentTime = 0;
        setAudioVolume('sound-effect2', 1.0*{global_volume});
        window.parent.Pause('sound-effect1');
        window.parent.Pause('sound-effect3');
        window.parent.Pause('sound-effect4');
        audio.play().catch(err => {{
            alert("😥 胜利音效播放失败～");
        }});
    }};

    window.parent.playSound3 = function() {{
        const audio = document.getElementById('sound-effect3');
        audio.currentTime = 0;
        setAudioVolume('sound-effect3', 1.0*{global_volume});
        window.parent.Pause('sound-effect1');
        window.parent.Pause('sound-effect2');
        window.parent.Pause('sound-effect4');
        audio.play().catch(err => {{
            alert("😥 失败音效播放失败～");
        }});
    }};

    window.parent.playSound4 = function() {{
        const audio = document.getElementById('sound-effect4');
        audio.currentTime = 0;
        setAudioVolume('sound-effect4', 1.0*{global_volume});
        window.parent.Pause('sound-effect1');
        window.parent.Pause('sound-effect2');
        window.parent.Pause('sound-effect3');
        audio.play().catch(err => {{
            alert("😥 失败音效播放失败～");
        }});
    }};

    window.parent.playSound5 = function() {{
        const audio = document.getElementById('sound-effect5');
        audio.currentTime = 0;
        setAudioVolume('sound-effect5', 1.0*{global_volume});
        audio.play().catch(err => {{
            alert("😥 失败音效播放失败～");
        }});
    }};

    window.parent.playSound0 = function(n) {{
        audio_name = 'sound-effect'+ n ;
        const audio = document.getElementById(audio_name);
        audio.currentTime = 0;
        setAudioVolume(audio_name, 1.0*{global_volume});
        audio.play().catch(err => {{
            alert("😥 失败音效播放失败～");
        }});
    }};

    window.parent.playSound_pro = function(n) {{
        audio_name = 'sound-effect'+ n ;
        const audio = document.getElementById(audio_name);
        audio.currentTime = 0;
        for(let i = 1; i<= 10; i++){{
            audio_name1 ='sound-effect'+ i; 
            window.parent.Pause(audio_name1);
        }};
        setAudioVolume(audio_name, 1.0*{global_volume});
        audio.play().catch(err => {{
            alert("😥 失败音效播放失败～");
        }});
    }};

    window.parent.is_paused = function(name){{
        return name.paused;
    }}

    if({st.session_state.current_step1} == 2){{
        const audio1 = document.getElementById('sound-effect');
        if(audio1.paused) window.parent.playSound();
    }}
</script>
"""

# 渲染缓存后的音频组件（仅首次/音量变化时重新生成）
components.html(render_audio_html(st.session_state.global_volume), height=0)

# ========== 8. 封装JS调用函数（减少重复代码） ==========
def play_audio_js(audio_func):
    """封装音频播放的JS调用，精简重复代码"""
    components.html(f"""
    <script>
        window.parent.{audio_func};
    </script>
    """, height=0)

def pause_audio_js(audio_ids):
    """封装暂停音频的JS调用"""
    pause_cmds = "\n".join([f"window.parent.Pause('{aid}');" for aid in audio_ids])
    components.html(f"""
    <script>
        {pause_cmds}
    </script>
    """, height=0)

# ========== 9. 游戏逻辑（完全保留原有交互，仅优化调用方式） ==========
col1, _ = st.columns([5, 5])
with col1:
    if st.session_state.current_step1 == 1:
        st.markdown("开始游戏吗？<br>(关音菩萨提醒您，前方记得调小音量)", unsafe_allow_html=True)
        if st.button("《千恋万花》，启动！"):
            st.session_state.current_step1 = 2
            st.session_state.current_step = 1
            st.session_state.fail = 2
            st.rerun()

if st.session_state.current_step == 1:
    if st.session_state.fail == 2:
        pause_audio_js(['sound-effect11', 'sound-effect4'])
        play_audio_js("playSound()")
        st.session_state.fail = 1
    st.image(load_image_cached(IMAGE_PATHS["m9"]), width=300, caption="狗修金又在看奇怪的网站了！")
    st.write("这是一个丛雨，要摸头吗")
    if st.button("👋摸摸头"):
        st.session_state.current_step = 2.1
        st.rerun()
    elif st.button("不要!!!"):
        st.session_state.current_step = 2.2
        st.rerun()

elif st.session_state.current_step == 2.1 :
    st.image(load_image_cached(IMAGE_PATHS["m5"]), width=300, caption="狗修金？")
    play_audio_js("playSound1()")
    if st.button("继续摸"):
        st.session_state.current_step = 3
        st.rerun()
    elif st.button("不摸了,寸止"):
        st.session_state.current_step = 2.2
        st.rerun()

elif st.session_state.current_step == 2.2:
    st.image(load_image_cached(IMAGE_PATHS["m2"]), width=300, caption="狗！修！金！！！")
    play_audio_js("playSound2()")
    if st.button("吓我一跳,释放时间回溯忍术！"):
        st.session_state.current_step = 1
        st.rerun()
    elif st.button("被幼刀吓哭了，那只能摸了😭😭😭"):
        st.session_state.current_step = 2.1
        st.rerun()
    elif st.button("不、不摸...那咋啦？"):
        st.session_state.current_step = -1
        st.rerun()

elif st.session_state.current_step == 3:
    st.image(load_image_cached(IMAGE_PATHS["m3"]), width=300, caption="狗~修~金~💗")
    play_audio_js("playSound3()")
    if st.button("无线摸头摸个爽！"):
        st.session_state.current_step = 2.1
        st.rerun()
    elif st.button("不摸了,她总不能是滑动变阻器吧"):
        st.session_state.current_step = 2.2
        st.rerun()

elif st.session_state.current_step == -1:
    pause_audio_js(['sound-effect'])
    play_audio_js("playSound_pro('11')")
    play_audio_js("playSound4()")
    st.markdown("丛雨吃掉了你的手指！<br>游戏结束！", unsafe_allow_html=True)
    st.image(load_image_cached(IMAGE_PATHS["m4"]), width=300, caption="豪赤😋！！！")
    if st.button("第三炸弹，败者食尘！"):
        pause_audio_js(['sound-effect11', 'sound-effect4'])
        play_audio_js("playSound()")
        st.session_state.current_step = 1
        st.session_state.fail = 2
        st.rerun()

# ========== 10. Ciallo按钮（逻辑不变，精简调用） ==========
st.image(load_image_cached(IMAGE_PATHS["ciallo"]), width=300, caption="雑魚柚子厨~💗💗💗")
if st.button("点击Ciallo~ (∠・ω< )⌒★"):
    num = rd.randint(1, 6)
    play_audio_js(f"playSound0('{num+4}')")  # 1→5, 2→6...6→10，和原逻辑一致