import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import random as rd

# ========== 1. 优先初始化所有session_state（调整顺序） ==========
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "current_step1" not in st.session_state:
    st.session_state.current_step1 = 1
if "global_volume" not in st.session_state:
    st.session_state.global_volume = 0.5
if "fail" not in st.session_state:
    st.session_state.fail = 1
# ========== 2. 页面配置（放顶部更规范） ==========
st.set_page_config(
    page_title="丛雨摸头模拟器",
    page_icon="./image/murasame7.jpg",
)
st.title("丛雨摸头模拟器")

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

# ========== 3. Base64转换函数（精简冗余） ==========
def sound_to_base64(sound_path):
    if not os.path.exists(sound_path):
        st.error(f"😥 音效文件找不到！路径：{sound_path}")
        return ""
    with open(sound_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# 精简：只定义4个音效路径（删除冗余的SOUND_PATH）
# 替换成你的音效路径
SOUND_PATH = "./audio/song.mp3"
SOUND_PATH1 = "./audio/Murasame1.mp3"
SOUND_PATH2 = "./audio/Murasame2.mp3"
SOUND_PATH3 = "./audio/Murasame3.mp3"
SOUND_PATH4 = "./audio/Murasame4.mp3"
SOUND_PATH5 = "./audio/ciallo1.mp3"
SOUND_PATH6 = "./audio/ciallo2.mp3"
SOUND_PATH7 = "./audio/ciallo3.mp3"
SOUND_PATH8 = "./audio/ciallo4.mp3"
SOUND_PATH9 = "./audio/ciallo5.mp3"
SOUND_PATH10 = "./audio/ciallo6.mp3"
SOUND_PATH11 = "./audio/man.mp3"



# 转换所有音效（删除冗余的sound_base64）
sound_base64 = sound_to_base64(SOUND_PATH)
sound_base64_1 = sound_to_base64(SOUND_PATH1)
sound_base64_2 = sound_to_base64(SOUND_PATH2)
sound_base64_3 = sound_to_base64(SOUND_PATH3)
sound_base64_4 = sound_to_base64(SOUND_PATH4)
sound_base64_5 = sound_to_base64(SOUND_PATH5)
sound_base64_6 = sound_to_base64(SOUND_PATH6)
sound_base64_7 = sound_to_base64(SOUND_PATH7)
sound_base64_8 = sound_to_base64(SOUND_PATH8)
sound_base64_9 = sound_to_base64(SOUND_PATH9)
sound_base64_10 = sound_to_base64(SOUND_PATH10)
sound_base64_11 = sound_to_base64(SOUND_PATH11)

# 生成Base64 URL
sound_src = f"data:audio/mp3;base64,{sound_base64}"
sound_src1 = f"data:audio/mp3;base64,{sound_base64_1}"
sound_src2 = f"data:audio/mp3;base64,{sound_base64_2}"
sound_src3 = f"data:audio/mp3;base64,{sound_base64_3}"
sound_src4 = f"data:audio/mp3;base64,{sound_base64_4}"
sound_src5 = f"data:audio/mp3;base64,{sound_base64_5}"
sound_src6 = f"data:audio/mp3;base64,{sound_base64_6}"
sound_src7 = f"data:audio/mp3;base64,{sound_base64_7}"
sound_src8 = f"data:audio/mp3;base64,{sound_base64_8}"
sound_src9 = f"data:audio/mp3;base64,{sound_base64_9}"
sound_src10 = f"data:audio/mp3;base64,{sound_base64_10}"
sound_src11 = f"data:audio/mp3;base64,{sound_base64_11}"
# ========== 4. 修复音频组件的语法/ID错误 ==========
components.html(f"""
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
<audio id="sound-effect4" style="display: none;">  <!-- 修复：唯一ID -->
    <source src="{sound_src4}" type="audio/mp3">
</audio>
<audio id="sound-effect5" style="display: none;">  <!-- 修复：唯一ID -->
    <source src="{sound_src5}" type="audio/mp3">
</audio>
</audio>
<audio id="sound-effect6" style="display: none;">  <!-- 修复：唯一ID -->
    <source src="{sound_src6}" type="audio/mp3">
</audio>
</audio>
<audio id="sound-effect7" style="display: none;">  <!-- 修复：唯一ID -->
    <source src="{sound_src7}" type="audio/mp3">
</audio>
</audio>
<audio id="sound-effect8" style="display: none;">  <!-- 修复：唯一ID -->
    <source src="{sound_src8}" type="audio/mp3">
</audio>
</audio>
<audio id="sound-effect9" style="display: none;">  <!-- 修复：唯一ID -->
    <source src="{sound_src9}" type="audio/mp3">
</audio>
</audio>
<audio id="sound-effect10" style="display: none;">  <!-- 修复：唯一ID -->
    <source src="{sound_src10}" type="audio/mp3">
</audio>
<audio id="sound-effect11" style="display: none;">  <!-- 修复：唯一ID -->
    <source src="{sound_src11}" type="audio/mp3">
</audio>
<script>
    // 通用函数：更新所有音频的整体音量（核心！）
    function updateGlobalVolume(volume) {{
        const allAudioIds = ['sound-effect','sound-effect1', 'sound-effect2', 'sound-effect3', 'sound-effect4'];
        allAudioIds.forEach(audioId => {{
            const audio = document.getElementById(audioId);
            if (audio) {{
                audio.volume = volume; // 同步音量到每个音频
            }}
        }});
        console.log(`✅ 整体音量已更新为：${{volume*100}}%`);
    }}

    // 初始化：页面加载时同步当前音量
    updateGlobalVolume({st.session_state.global_volume});

// 定义通用音量设置函数（可复用）
    function setAudioVolume(audioId, volume) {{
        const audio = document.getElementById(audioId);
        audio.volume = volume; // 设置音量（0-1）
        console.log(`✅ ${{audioId}} 音量设为：${{volume*100}}%`);
    }}
    // 修复：playSound3闭合，playSound4独立定义
    window.parent.playSound = function() {{
        const audio = document.getElementById('sound-effect');
        audio.currentTime = 0;
        setAudioVolume('sound-effect', 0.1*{st.session_state.global_volume});
        audio.play().catch(err => {{
            alert("😥 启动音效播放失败，请检查音频权限～");
        }});
    }};
    // 核心新增：暂停指定音频的函数
    window.parent.Pause = function(audioId, resetPosition = true) {{
        // 1. 查找指定ID的音频元素
        const audio = document.getElementById(audioId);
        if (!audio) {{
            return;
        }}
        // 2. 检查是否正在播放
        if (audio.paused) {{
            return;
        }}
        // 3. 暂停音频
        audio.pause();
        // 4. 可选：重置到开头（默认true）
        if (resetPosition) {{
            audio.currentTime = 0;
        }}
        console.log(`✅ 已暂停指定音频：${{audioId}}`);

    }};

    window.parent.playSound1 = function() {{
        const audio = document.getElementById('sound-effect1');
        audio.currentTime = 0;
        setAudioVolume('sound-effect1', 1.0 * {st.session_state.global_volume});
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
        setAudioVolume('sound-effect2', 1.0*{st.session_state.global_volume});
        window.parent.Pause('sound-effect1');
        window.parent.Pause('sound-effect3');
        window.parent.Pause('sound-effect4');
        audio.play().catch(err => {{
            alert("😥 胜利音效播放失败～");
        }});
    }};

    window.parent.playSound3 = function() {{  // 修复：闭合函数
        const audio = document.getElementById('sound-effect3');
        audio.currentTime = 0;
        setAudioVolume('sound-effect3', 1.0*{st.session_state.global_volume});
        window.parent.Pause('sound-effect1');
        window.parent.Pause('sound-effect2');
        window.parent.Pause('sound-effect4');
        audio.play().catch(err => {{
            alert("😥 失败音效播放失败～");
        }});
    }};  // 新增：playSound3的闭合括号

    window.parent.playSound4 = function() {{  // 修复：独立定义
        const audio = document.getElementById('sound-effect4');  // 修复：调用正确ID
        audio.currentTime = 0;
        setAudioVolume('sound-effect4', 1.0*{st.session_state.global_volume});
        window.parent.Pause('sound-effect1');
        window.parent.Pause('sound-effect2');
        window.parent.Pause('sound-effect3');
        audio.play().catch(err => {{
            alert("😥 失败音效播放失败～");
        }});
    }};
        window.parent.playSound5 = function() {{  // 修复：独立定义
        const audio = document.getElementById('sound-effect5');  // 修复：调用正确ID
        audio.currentTime = 0;
        setAudioVolume('sound-effect5', 1.0*{st.session_state.global_volume});
        audio.play().catch(err => {{
            alert("😥 失败音效播放失败～");
        }});
    }};
    
        window.parent.playSound0 = function(n) {{  // 修复：独立定义
        audio_name = 'sound-effect'+ n ;
        const audio = document.getElementById(audio_name);  // 修复：调用正确ID
        audio.currentTime = 0;
        
        setAudioVolume(audio_name, 1.0*{st.session_state.global_volume});
        audio.play().catch(err => {{
            alert("😥 失败音效播放失败～");
        }});
    }};
    
        window.parent.playSound_pro = function(n) {{  // 修复：独立定义
        audio_name = 'sound-effect'+ n ;
        const audio = document.getElementById(audio_name);  // 修复：调用正确ID
        audio.currentTime = 0;
        
        for(let i = 1; i<= 10; i++){{
        audio_name1 ='sound-effect'+ i; 
        window.parent.Pause(audio_name1);
        }};
        setAudioVolume(audio_name, 1.0*{st.session_state.global_volume});
        audio.play().catch(err => {{
            alert("😥 失败音效播放失败～");
        }});
    }};
    window.parent.is_paused = function(name){{
    if (name.paused)return true;
    else return false;
    }}
    
    if({st.session_state.current_step1} == 2){{
      const audio1 = document.getElementById('sound-effect');
      if(audio1.paused){{
          window.parent.playSound();
      }}       
    }}
</script>
""", height=0)

# ========== 5. 修复按钮逻辑的缩进/注释 ==========
col1, _ = st.columns([5, 5])
with col1:
    if st.session_state.current_step1 == 1:
        st.markdown("开始游戏吗？<br>(关音菩萨提醒您，前方记得调小音量)", unsafe_allow_html=True)
        if st.button("《千恋万花》，启动！"):
            st.session_state.current_step1 = 2
            st.session_state.current_step = 1
            # 修复：注释移到内部，缩进更清晰
            components.html("""
            <script>
                window.parent.playSound();
            </script>
            """, height=0)
            st.rerun()

# ========== 6. 游戏步骤逻辑（仅修复换行符，其余保留） ==========
if st.session_state.current_step == 1:
    if st.session_state.fail == 2:
        components.html("""
        <script>
            const audio1 = document.getElementById('sound-effect');
            window.parent.Pause('sound-effect11');
            window.parent.Pause('sound-effect4');  
            window.parent.playSound();
        </script>
         """, height=0)
        st.session_state.fail = 1
    st.image("./image/murasame9.jpg", width=300, caption="狗修金又在看奇怪的网站了！")
    st.write("这是一个丛雨，要摸头吗")
    if st.button("👋摸摸头"):
        st.session_state.current_step = 2.1
        # 兼容旧版本：替换st.rerun()为st.experimental_rerun()（如果版本低）
        st.rerun()
    elif st.button("不要!!!"):
        st.session_state.current_step = 2.2
        st.rerun()

elif st.session_state.current_step == 2.1 :
    st.image("./image/murasame5.webp", width=300, caption="狗修金？")
    components.html("""
        <script>
            window.parent.playSound1();            
        </script>
    """, height=0)
    if st.button("继续摸"):
        st.session_state.current_step = 3
        st.rerun()
    elif st.button("不摸了,寸止"):
        st.session_state.current_step = 2.2
        st.rerun()

elif st.session_state.current_step == 2.2:
    st.image("./image/murasame2.jpg", width=300, caption="狗！修！金！！！")
    components.html("""
        <script>
            window.parent.playSound2();
        </script>
    """, height=0)
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
    st.image("./image/murasame3.jpg", width=300, caption="狗~修~金~💗")
    components.html("""
        <script>
            window.parent.playSound3();
        </script>
    """, height=0)
    if st.button("无线摸头摸个爽！"):
        st.session_state.current_step = 2.1
        st.rerun()
    elif st.button("不摸了,她总不能是滑动变阻器吧"):
        st.session_state.current_step = 2.2
        st.rerun()

elif st.session_state.current_step == -1:
    components.html("""
        <script>
            window.parent.Pause('sound-effect');
            window.parent.playSound_pro("11");
            window.parent.playSound4();
        </script>
    """, height=0)
    # 修复：换行符无效问题
    st.markdown("丛雨吃掉了你的手指！<br>游戏结束！", unsafe_allow_html=True)
    st.image("./image/murasame4.webp", width=300, caption="豪赤😋！！！")
    if st.button("第三炸弹，败者食尘！"):
        components.html("""
        <script>
            window.parent.Pause('sound-effect11');
            window.parent.Pause('sound-effect4');  
            window.parent.playSound();
        </script>
         """, height=0)
        st.session_state.current_step = 1
        st.session_state.fail = 2
        st.rerun()



st.image(
    "./image/ciallo.jpg",
    width=300, caption = "雑魚柚子厨~💗💗💗")
if st.button("点击Ciallo~ (∠・ω< )⌒★"):
    num = rd.randint(1, 6)

    if num == 1:
        components.html("""
                    <script>     
                        window.parent.playSound0("5");
                    </script>
            """, height=0)
    elif num == 2:
        components.html("""
                    <script>
                        window.parent.playSound0("6");
                    </script>
            """, height=0)
    elif num == 3:
        components.html("""
                    <script>
                        window.parent.playSound0("7");
                    </script>
            """, height=0)
    elif num == 4:
        components.html("""
                    <script>
                        window.parent.playSound0("8");
                    </script>
            """, height=0)
    elif num == 5:
        components.html("""
                    <script>
                        window.parent.playSound0("9");
                    </script>
            """, height=0)
    elif num == 6:
        components.html("""
                    <script>
                        window.parent.playSound0("10");
                    </script>
            """, height=0)

