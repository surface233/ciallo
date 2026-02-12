import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import random as rd
import uuid  # 生成唯一音频ID

# ========== 1. 初始化Session State（新增好感度初始化） ==========
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "current_step1" not in st.session_state:
    st.session_state.current_step1 = 1
if "global_volume" not in st.session_state:
    st.session_state.global_volume = 0.5
if "fail" not in st.session_state:
    st.session_state.fail = 1
# 新增：初始化好感度（初始值50，范围0-100）
if "affection" not in st.session_state:
    st.session_state.affection = 50

# ========== 2. 页面配置（不变） ==========
st.set_page_config(
    page_title="丛雨摸头模拟器",
    page_icon="./image/murasame7.jpg",
)
st.title("丛雨摸头模拟器")

# ========== 3. 音量滑块（不变） ==========
if st.session_state.current_step1 == 1:
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

# ========== 3.5 新增：好感度可视化（核心新增） ==========
# 只在游戏启动后显示好感度
if st.session_state.current_step1 != 1:
    st.subheader("💖 丛雨好感度")
    # 条状进度条可视化
    affection_progress = st.progress(st.session_state.affection)
    # 显示具体数值（更直观）
    st.caption(f"当前好感度：{st.session_state.affection}/100")
    # 好感度状态提示（可选，增强体验）
    if st.session_state.affection >= 80:
        st.success("✨ 丛雨甚至想0721了！")
    elif st.session_state.affection >= 50:
        st.info("😊 丛雨觉得你风韵犹存~")
    elif st.session_state.affection >= 20:
        st.warning("😐 丛雨正在准备铁拳...")
    else:
        st.error("💢 丛雨即将降下神罚！")

# ========== 4. 核心：多音频播放+停止框架（不变） ==========
def sound_to_base64(sound_path):
    """按需读取音频文件并转成Base64"""
    if not os.path.exists(sound_path):
        st.warning(f"⚠️ 音效文件未找到：{sound_path}（可忽略，不影响游戏）")
        return ""
    with open(sound_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_song_base64():
    """预处理song.mp3，转换为Base64编码（不存在则返回空字符串）"""
    song_path = "./audio/song.mp3"
    if not os.path.exists(song_path):
        st.warning(f"⚠️ 音效文件未找到：{song_path}（可忽略，不影响游戏）")
        return ""
    with open(song_path, "rb") as f:
        return base64.b64encode(f.read()).decode()



# 提前生成song.mp3的Base64编码
song_base64 = get_song_base64()
# 初始化多音频播放/停止的JS
components.html(f"""
<script>
    // 存储所有活跃的音频实例（支持多音频叠加）
    let audioInstances = {{}};
    // 映射音频文件路径 → 对应的实例ID列表（用于精准停止）
    let audioPathToIds = {{}};
    // 预处理的song.mp3 Base64数据
    const songBase64 = "{song_base64}";
    const songAudioPath = "./audio/song.mp3";

    // 播放音频（支持叠加，记录路径和实例ID映射）
    window.parent.playAudioInstance = function(audioPath, audioId, b64Data, volume) {{
        // 创建新音频实例
        const audio = new Audio(`data:audio/mp3;base64,${{b64Data}}`);
        audio.volume = volume;
        // 记录实例和路径映射
        audioInstances[audioId] = audio;
        if (!audioPathToIds[audioPath]) {{
            audioPathToIds[audioPath] = [];
        }}
        audioPathToIds[audioPath].push(audioId);
        // 播放完成后自动清理
        audio.onended = function() {{
            delete audioInstances[audioId];
            // 从路径映射中移除
            audioPathToIds[audioPath] = audioPathToIds[audioPath].filter(id => id !== audioId);
            if (audioPathToIds[audioPath].length === 0) {{
                delete audioPathToIds[audioPath];
            }}
        }};
        // 播放音频
        audio.play().catch(err => {{
            console.log("音效播放提示（浏览器限制）：", err);
        }});
    }};

    // 核心修改：专门播放song.mp3的函数，音量为全局音量×10%
    window.parent.playSongAudio = function(globalVolume) {{
        if (!songBase64) {{
            console.log("song.mp3 Base64数据为空，跳过播放");
            return;
        }}
        // 生成唯一ID
        const audioId = "{str(uuid.uuid4())}";
        // 音量 = 全局音量 × 0.1
        const finalVolume = globalVolume * 0.1;
        // 调用原有播放逻辑，关联song.mp3路径（方便后续停止）
        window.parent.playAudioInstance(songAudioPath, audioId, songBase64, finalVolume);
    }};

    // 停止指定路径的音频
    window.parent.stopAudioByPath = function(audioPath) {{
        if (audioPathToIds[audioPath]) {{
            // 停止该路径下所有实例
            audioPathToIds[audioPath].forEach(audioId => {{
                if (audioInstances[audioId]) {{
                    audioInstances[audioId].pause();
                    audioInstances[audioId].currentTime = 0; // 重置播放进度
                    delete audioInstances[audioId];
                }}
            }});
            // 清空该路径的映射
            delete audioPathToIds[audioPath];
            console.log(`✅ 已停止所有【${{audioPath}}】音频`);
        }}
    }};

    // 暂停指定ID的音频（保留）
    window.parent.pauseAudioInstance = function(audioId) {{
        if (audioInstances[audioId]) {{
            audioInstances[audioId].pause();
            audioInstances[audioId].currentTime = 0;
            delete audioInstances[audioId];
            // 从路径映射中移除
            for (const path in audioPathToIds) {{
                audioPathToIds[path] = audioPathToIds[path].filter(id => id !== audioId);
                if (audioPathToIds[path].length === 0) {{
                    delete audioPathToIds[path];
                }}
            }}
        }}
    }};

    // 暂停所有音频（保留）
    window.parent.pauseAllAudio = function() {{
        Object.keys(audioInstances).forEach(id => {{
            audioInstances[id].pause();
            audioInstances[id].currentTime = 0;
        }});
        audioInstances = {{}};
        audioPathToIds = {{}}; // 清空路径映射
    }};
</script>
""", height=0)

# ========== 5. 封装播放/停止函数（不变） ==========
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
    # 调用JS播放（传递路径，用于后续停止）
    components.html(f"""
    <script>
        window.parent.playAudioInstance("{audio_path}", "{audio_unique_id}", "{b64_data}", {final_volume});
    </script>
    """, height=0)

def stop_audio(audio_path):
    """
    停止指定路径的音频（精准停止，不影响其他音频）
    :param audio_path: 音频文件路径（如 "./audio/song.mp3"）
    """
    components.html(f"""
    <script>
        window.parent.stopAudioByPath("{audio_path}");
    </script>
    """, height=0)

def pause_all_audio():
    """停止所有音频"""
    components.html("""
    <script>
        window.parent.pauseAllAudio();
    </script>
    """, height=0)

# ========== 6. 完整游戏逻辑（新增好感度更新） ==========
col1, _ = st.columns([5, 5])
with col1:
    if st.session_state.current_step1 == 1:

        st.markdown("开始游戏吗？<br>(关音菩萨提醒您，前方记得调小音量)", unsafe_allow_html=True)
        if st.button("《千恋万花》，启动！"):
            st.session_state.current_step1 = 2
            st.session_state.current_step = 1
            # song.mp3 固定10%音量
            st.session_state.fail = 2
            st.rerun()

# 步骤1：初始选择（新增好感度变化）
if 0 < st.session_state.affection < 100:
    if st.session_state.current_step == 1:
        st.image("./image/murasame9.jpg", width=300, caption="狗修金又在看奇怪的网站了！")
        st.write("这是一个丛雨，要摸头吗")
        # 摸头：好感度+10（上限100）
        if st.session_state.fail == 2:
            # 先停止旧的song.mp3，再播放新的
            pause_all_audio()
            play_audio("./audio/song.mp3", custom_volume=0.1)
            st.session_state.fail = 1

        if st.button("👋摸摸头"):
            st.session_state.affection = min(st.session_state.affection + 10, 100)
            st.session_state.current_step = 2.1
            st.rerun()
        # 拒绝：好感度-15（下限0）
        elif st.button("我也要摸吗？"):
            st.session_state.affection = max(st.session_state.affection - 15, 0)
            st.session_state.current_step = 2.2
            st.rerun()

    # 步骤2.1：摸头分支（新增好感度变化）
    elif st.session_state.current_step == 2.1:
        st.image("./image/murasame5.webp", width=300, caption="狗修金？")
        st.write("我去，摸头起手？你高低是个三千！")
        stop_audio("./audio/Murasame2.mp3")
        stop_audio("./audio/Murasame3.mp3")
        stop_audio("./audio/Murasame4.mp3")
        play_audio("./audio/Murasame1.mp3")
        # 继续摸：好感度+8
        if st.button("嘿嘿，幼刀酱~继续摸"):
            st.session_state.affection = min(st.session_state.affection + 8, 100)
            st.session_state.current_step = 3
            st.rerun()
        # 不摸了：好感度-5
        elif st.button("我好像踩到地雷了，寸止！"):
            st.session_state.affection = max(st.session_state.affection - 5, 0)
            st.session_state.current_step = 2.2
            st.rerun()

    # 步骤2.2：拒绝摸头分支（新增好感度变化）
    elif st.session_state.current_step == 2.2:
        st.image("./image/murasame2.jpg", width=300, caption="狗！修！金！！！")
        stop_audio("./audio/Murasame1.mp3")
        stop_audio("./audio/Murasame3.mp3")
        stop_audio("./audio/Murasame4.mp3")
        play_audio("./audio/Murasame2.mp3")
        st.write("屏幕前的各位觉得我能活下来吗？")
        # 时间回溯：好感度-8
        if st.button("吓我一跳,释放时间回溯忍术！"):
            st.session_state.affection = max(st.session_state.affection - 10, 0)
            st.session_state.current_step = 1
            st.rerun()
        # 妥协摸头：好感度+5
        elif st.button("幼刀酱是个纯小子，那只能摸头了😭😭😭"):
            st.session_state.affection = min(st.session_state.affection + 5, 100)
            st.session_state.current_step = 2.1
            st.rerun()
        # 坚持不摸：好感度-20
        elif st.button("区区太平公主，我避她锋芒？"):
            st.session_state.affection = max(st.session_state.affection - 20, 0)
            st.session_state.current_step = -1
            st.rerun()
        elif st.button("666还有互动环节"):
            components.html("""
                        <script>
                            // 打开B站指定页面（可替换为任意B站链接）
                            window.open("https://www.bilibili.com/video/BV1GJ411x7h7/?spm_id_from=333.337.search-card.all.click&vd_source=03866106963f94515a9608a07c42a978", "_blank");
                        </script>
                        """, height=0)
            st.session_state.current_step = 114514
            st.session_state.affection = 78
            st.rerun()



    # 步骤3：继续摸头分支（新增好感度变化）
    elif st.session_state.current_step == 3:
        st.image("./image/murasame3.jpg", width=300, caption="狗~修~金~💗")
        stop_audio("./audio/Murasame1.mp3")
        stop_audio("./audio/Murasame2.mp3")
        stop_audio("./audio/Murasame4.mp3")
        play_audio("./audio/Murasame3.mp3")
        # 无限摸头：好感度+10
        if st.button("无线摸头摸个爽！"):
            st.session_state.affection = min(st.session_state.affection + 10, 100)
            st.session_state.current_step = 2.1
            st.rerun()
        # 停止摸头：好感度-10
        elif st.button("不摸了,她总不能是滑动变阻器吧"):
            st.session_state.affection = max(st.session_state.affection - 10, 0)
            st.session_state.current_step = 2.2
            st.rerun()

    # 步骤-1：游戏结束分支（新增好感度重置）
    elif st.session_state.current_step == -1 or st.session_state.affection <= 0:
        # 停止之前的所有音频，再播放结束音效
        pause_all_audio()
        play_audio("./audio/Murasame4.mp3")
        play_audio("./audio/man.mp3")
        st.title("丛雨吃掉了你的手指！")
        st.title("游戏结束！")
        st.write("我嘞个不摸")
        st.image("./image/murasame4.webp", width=300, caption="豪赤😋！！！")
        st.image("./image/murasame1.jpg",width=300,caption="啧，果然是小雑魚~" )

        # 重置游戏：好感度恢复初始值50
        if st.button("第三炸弹，败者食尘！"):
            # 精准停止结束音效，再播放启动音效
            stop_audio("./audio/Murasame4.mp3")
            stop_audio("./audio/man.mp3")
            play_audio("./audio/song.mp3", custom_volume=0.1)
            st.session_state.affection = 50  # 重置好感度
            st.session_state.current_step = 1
            st.session_state.fail = 2
            st.rerun()

        if st.button("退出游戏"):
            components.html("""
                    <script>
                        // 打开B站指定页面（可替换为任意B站链接）
                        window.open("https://www.bilibili.com/video/BV1GJ411x7h7/?spm_id_from=333.337.search-card.all.click&vd_source=03866106963f94515a9608a07c42a978", "_blank");
                    </script>
                    """, height=0)
            st.session_state.current_step = 114514
            st.session_state.affection = 78
            st.rerun()

    elif st.session_state.current_step == 114514:
        stop_audio("./audio/Murasame4.mp3")
        stop_audio("./audio/man.mp3")
        pause_all_audio()
        st.title("你 被 骗 了 ! ! !")
        st.markdown("走流程还是自己吃？https://www.bilibili.com/video/BV1GJ411x7h7/?spm_id_from=333.337.search-card.all.click&vd_source=03866106963f94515a9608a07c42a978")
        if st.button("入口传送门"):
            play_audio("./audio/lemon.mp3",custom_volume=0.6)
            st.markdown("自己刷新？")

    # ========== 7. Ciallo彩蛋按钮 + 停止彩蛋音效 ==========
    if st.session_state.current_step1 == 1 or st.session_state.current_step == 1:
        st.image("./image/ciallo.jpg", width=300, caption="雑魚柚子厨~💗💗💗")
        if st.button("点击Ciallo~ (∠・ω< )⌒★"):
            num = rd.randint(1, 6)
            play_audio(f"./audio/ciallo{num}.mp3")

elif st.session_state.affection == 100:
    st.title("游戏胜利！")
    st.title("你简直就是旮旯给木之神！")
    st.write("丛雨被你攻略了！请你吃丛雨丸😋")
    pause_all_audio()
    st.image(
        "./image/murasame8.jpg",width = 300, caption = "嘿嘿~ 狗修金💗" )
    play_audio("./audio/Murasame5.mp3")
    play_audio("./audio/song1.mp3")



    if st.button("666还有第二关"):
        st.session_state.current_step = 1
        st.session_state.fail = 2
        st.session_state.affection = 50
        st.rerun()
    if st.button("退出游戏"):
        components.html("""
            <script>
                // 打开B站指定页面（可替换为任意B站链接）
                window.open("https://www.bilibili.com/video/BV1GJ411x7h7/?spm_id_from=333.337.search-card.all.click&vd_source=03866106963f94515a9608a07c42a978", "_blank");
            </script>
            """, height=0)
        st.session_state.current_step = 114514
        st.session_state.affection = 78
        st.rerun()



    st.image("./image/ciallo.jpg", width=300, caption="原神牛逼💗💗💗")

elif st.session_state.affection == 0:
    pause_all_audio()
    play_audio("./audio/Murasame4.mp3")
    play_audio("./audio/man.mp3")
    st.title("丛雨吃掉了你的手指！")
    st.title("游戏结束！")
    st.image("./image/murasame4.webp", width=300, caption="豪赤😋！！！")
    st.image("./image/murasame1.jpg", width=300, caption="我鸟都不鸟你")

    # 重置游戏：好感度恢复初始值50
    if st.button("第三炸弹，败者食尘！"):
        # 精准停止结束音效，再播放启动音效
        stop_audio("./audio/Murasame4.mp3")
        stop_audio("./audio/man.mp3")
        play_audio("./audio/song.mp3", custom_volume=0.1)
        st.session_state.affection = 50  # 重置好感度
        st.session_state.current_step = 1
        st.session_state.fail = 2
        st.rerun()

    if st.button("退出游戏"):
        pause_all_audio()
        components.html("""
                <script>
                    // 打开B站指定页面（可替换为任意B站链接）
                    window.open("https://www.bilibili.com/video/BV1GJ411x7h7/?spm_id_from=333.337.search-card.all.click&vd_source=03866106963f94515a9608a07c42a978", "_blank");
                </script>
                """, height=0)
        st.session_state.current_step = 114514
        st.session_state.affection = 78
        st.rerun()
