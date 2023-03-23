import React, { PureComponent } from "react";
import {
    View,
    StyleSheet,
    Text,
    Image,
    ImageBackground,
    Dimensions,
    TouchableOpacity,
    Animated,
    LogBox
} from "react-native";
import Slider from '@react-native-community/slider'

import * as FileSystem from 'expo-file-system'

import { Audio } from 'expo-av';

import TextTicker from 'react-native-text-ticker'

import { AntDesign, Entypo, MaterialIcons } from '@expo/vector-icons';

import DigitalTimeString from "./DigitalTimeString";
import { observer } from "mobx-react";
import { PlayerQueue } from "../mobX/playerQUEUE";

const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;

export default observer(class AudioSlider extends PureComponent {

    constructor(props) {
        super(props);
        this.state = {
            playing: false,
            isExpanded: false,
            currentTime: 0, // miliseconds
            duration: 0,
            height: new Animated.Value(40),
            songIsSaved: false,
            image: null,
            sound: null,
            disableButtons: false
        }

        this.setSongIsSaved = this.setSongIsSaved.bind(this)

        this.setHeight = this.setHeight.bind(this)

        this.setCurrentTime = this.setCurrentTime.bind(this)

        this.expandPlayer = this.expandPlayer.bind(this)

        this.collapsPlayer = this.collapsPlayer.bind(this)
    };

    loadImage = async (id) => {
        try {
            const res = await fetch(
                'http://192.168.1.66:12345/track/get_picture/' + id,
                {
                    method: 'GET',
                    cache: 'no-cache'
                }
            )
            const data = await res.blob();
            this.setState({ image: URL.createObjectURL(data) })
            return;
        } catch (error) {
            console.error(error)
        }
    };

    blobToBase64(blob) {
        return new Promise((resolve, _) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(blob);
        });
    }

    loadSound = async (id) => {
        try {
            const res = await fetch(
                'http://192.168.1.66:12345/track/get_track_file/' + id,
                {
                    method: 'GET',
                    cache: 'no-cache',
                    cache: 'default',
                    headers: {
                        "Content-Type": "audio/mp3"
                    }
                }
            )
            const data = await res.blob();
            // this.setState({ sound: URL.createObjectURL(data) })

            //base64
            let base64 = await this.blobToBase64(data)

            const options = { encoding: FileSystem.EncodingType.Base64 };

            const testUri = FileSystem.documentDirectory + "sound.mp3";
            await FileSystem.writeAsStringAsync(testUri, base64.split(',')[1], options);

            const file = await FileSystem.getInfoAsync(
                FileSystem.documentDirectory + "sound.mp3"
            );

            // const UTI = 'audio/mp3'
            // await Sharing.shareAsync(file.uri, { UTI })

            this.setState({ sound: testUri })

            return;
        } catch (error) {
            console.error(error)
        }
    };

    setSongIsSaved(value) {
        this.setState({ songIsSaved: value })
    }

    setHeight(value) {
        this.setState({ height: value })
    }

    setCurrentTime(value) {
        this.setState({ currentTime: value })
    }

    expandPlayer() {
        Animated.timing(this.state.height, {
            toValue: -windowHeight + 35,
            useNativeDriver: false,
            duration: 300
        }).start()
        this.setState({ isExpanded: true })
    }

    collapsPlayer() {
        Animated.timing(this.state.height, {
            toValue: 40,
            useNativeDriver: false,
            duration: 300
        }).start()
        this.setState({ isExpanded: false })
    }

    mapAudioToCurrentTime = async () => {
        try {
            await this.soundObject.setPositionAsync(this.state.currentTime);
        } catch (error) {
        }

    }

    onPressPlayPause = async () => {
        if (this.state.playing) {
            await this.pause();
            return
        }
        try {
            await this.play();
        } catch (error) {
            console.log(error)
        }
    }

    play = async () => {
        try {
            await this.soundObject.playAsync();
        } catch (error) {
            console.log(error)
        }

        this.setState({ playing: true }) // This is for the play-button to go to play
    }

    pause = async () => {
        try {
            await this.soundObject.pauseAsync();
        } catch (error) {
            console.log(error)
        }

        this.setState({ playing: false }) // This is for the play-button to go to pause
    }

    playNextSong = async () => {
        await this.soundObject.unloadAsync()
        PlayerQueue.increaseCurrentTrack()

        if (PlayerQueue.isAlone) {
            this.setState({ disableButtons: true })
            this.pause()
            this.setCurrentTime(0)

            await this.soundObject.unloadAsync()

            this.loadImage(this.props.id)

            await this.loadSound(this.props.id)
            await this.soundObject.loadAsync({ uri: this.state.sound });

            const status = await this.soundObject.getStatusAsync();
            this.setState({ duration: status["durationMillis"] });

            this.mapAudioToCurrentTime()

            this.setState({ disableButtons: false })

            this.play()
        }
    }

    playPrevSong = async () => {
        await this.soundObject.unloadAsync()
        PlayerQueue.decreaseCurrentTrack()

        if (PlayerQueue.isAlone) {
            this.setState({ disableButtons: true })
            this.pause()
            this.setCurrentTime(0)

            await this.soundObject.unloadAsync()

            this.loadImage(this.props.id)

            await this.loadSound(this.props.id)
            await this.soundObject.loadAsync({ uri: this.state.sound });

            const status = await this.soundObject.getStatusAsync();
            this.setState({ duration: status["durationMillis"] });

            this.mapAudioToCurrentTime()

            this.setState({ disableButtons: false })

            this.play()
        }
    }

    runSlider = async () => {
        if (this.state.playing && this.state.duration > this.state.currentTime + 1000) {
            let prevTime = this.state.currentTime
            this.setState({ currentTime: prevTime + 1000 })
        } else {
            //on end of the song function
            if (this.state.playing) {

                this.playNextSong()
                // console.log('end of the song')
            }
        }
    }

    //Saving a song to the user lybrary
    changeTrackStatus() {
        if (this.songIsSaved) {

        }
    }

    async componentDidMount() {
        this.setState({ songIsSaved: PlayerQueue.getQueue.tracks[PlayerQueue.getCurrentTrack].added })
        this.setState({ disableButtons: true })
        await Audio.setIsEnabledAsync(true);
        this.soundObject = new Audio.Sound();

        await this.loadSound(this.props.id)
        await this.soundObject.loadAsync({ uri: this.state.sound });

        const status = await this.soundObject.getStatusAsync();
        this.setState({ duration: status["durationMillis"] });

        this.loadImage(this.props.id)

        setInterval(this.runSlider, 1000);
        this.setState({ disableButtons: false })
        this.play()
    }

    async componentDidUpdate(prevProps) {
        if (prevProps !== this.props) {
            this.setState({ songIsSaved: PlayerQueue.getQueue.tracks[PlayerQueue.getCurrentTrack].added })
            console.log(PlayerQueue.getQueue.tracks[PlayerQueue.getCurrentTrack])
            this.setState({ disableButtons: true })
            this.pause()
            this.setCurrentTime(0)

            await this.soundObject.unloadAsync()

            this.loadImage(this.props.id)

            await this.loadSound(this.props.id)
            await this.soundObject.loadAsync({ uri: this.state.sound });

            const status = await this.soundObject.getStatusAsync();
            this.setState({ duration: status["durationMillis"] });

            this.mapAudioToCurrentTime()
            this.setState({ disableButtons: false })
            this.play()
        }
    }

    async componentWillUnmount() {
        await this.soundObject.unloadAsync();
    }

    trackNameAmountOfSymbols = this.props.trackName.length

    render() {
        return (
            <View>
                {/* expanded player */}
                <Animated.View
                    style={{
                        height: windowHeight,
                        resizeMode: 'cover',
                        // top: -windowHeight + 35,
                        top: this.state.height,
                        width: windowWidth,
                        position: 'absolute',
                        zIndex: 2,
                        backgroundColor: 'black'
                    }}
                >
                    <ImageBackground
                        style={{
                            resizeMode: 'cover',
                            paddingTop: 40,
                            justifyContent: 'center',
                            alignItems: 'center',
                            flex: 1
                        }}
                        blurRadius={50}
                        source={{ uri: this.state.image }}
                    >
                        <View style={[styles.content, styles.expandedContainerStyle]}>
                            <TouchableOpacity style={{ position: 'absolute', right: 10, top: 10, zIndex: 1 }} onPress={this.collapsPlayer}>
                                <AntDesign name="close" size={35} color="white" />
                            </TouchableOpacity>

                            <View style={styles.expandedContainerStyle}>
                                <Image
                                    source={{ uri: this.state.image }}
                                    style={[styles.trackPhoto, {
                                        width: 300, height: 300
                                    }]} />

                                <View style={styles.expandedTrackInfo}>
                                    {this.trackNameAmountOfSymbols > 23 ?
                                        <View>
                                            <TextTicker
                                                style={{
                                                    width: 200,
                                                    color: 'white',
                                                    fontSize: 20,
                                                    fontFamily: 'Nunito-Bold',
                                                }}
                                                duration={10000}
                                                loop
                                                repeatSpacer={100}
                                                marqueeDelay={1000}
                                            >
                                                {this.props.trackName}
                                            </TextTicker>
                                            <Text numberOfLines={1} style={[styles.text, { opacity: 0.8, fontSize: 16 }]}>{this.props.trackAuthor}</Text>
                                        </View>
                                        :
                                        <View>
                                            <Text numberOfLines={1} style={styles.text}>{this.props.trackName}</Text>
                                            <Text numberOfLines={1} style={[styles.text, { opacity: 0.8, fontSize: 16 }]}>{this.props.trackAuthor}</Text>
                                        </View>
                                    }
                                    <TouchableOpacity style={{ height: '100%' }} onPress={async () => {
                                        this.setSongIsSaved(!this.state.songIsSaved)

                                        try {
                                            let path = 'http://192.168.1.66:12345/library/change_track_status/?library_id=' + 1 + '&track_id=' + PlayerQueue.getQueue.tracks[PlayerQueue.getCurrentTrack].id
                                            const callback = await fetch(
                                                path,
                                                {
                                                    method: 'POST',
                                                }
                                            );

                                            return callback

                                        } catch (error) {
                                            console.error(error);
                                        }
                                    }}>
                                        {
                                            this.state.songIsSaved
                                                ?
                                                <AntDesign name="minuscircleo" size={24} color="white" />
                                                :
                                                <AntDesign name="pluscircleo" size={24} color="white" />
                                        }
                                    </TouchableOpacity>

                                </View>

                                <Slider
                                    minimumValue={0}
                                    maximumValue={this.state.duration}
                                    step={1000}
                                    minimumTrackTintColor="#FF0054"
                                    style={[styles.slider, { width: '90%' }]}
                                    value={this.state.currentTime}
                                    onSlidingComplete={
                                        time => {
                                            this.setCurrentTime(time)
                                            this.soundObject.setPositionAsync(time)
                                        }
                                    }
                                />

                                <View style={{
                                    flex: 0,
                                    width: '90%',
                                    flexDirection: "row",
                                    alignItems: 'center',
                                    justifyContent: "space-between",
                                }}>
                                    <DigitalTimeString time={this.state.currentTime} />
                                    <DigitalTimeString time={this.state.duration} />
                                </View>

                                <View style={styles.expandedControlBtns}>
                                    <TouchableOpacity
                                        style={styles.playBTN}
                                        onPress={() => { this.playPrevSong() }}
                                    >
                                        <AntDesign name="banckward" size={40} color="white" />
                                    </TouchableOpacity>
                                    <TouchableOpacity
                                        disabled={this.state.disableButtons}
                                        style={styles.playBTN}
                                        onPress={this.onPressPlayPause}
                                    >
                                        {
                                            this.state.playing
                                                ?
                                                <MaterialIcons name="pause" size={50} color="white" />
                                                :
                                                <Entypo name="controller-play" size={50} color="white" />
                                        }
                                    </TouchableOpacity>
                                    <TouchableOpacity
                                        style={styles.playBTN}
                                        onPress={() => { this.playNextSong() }}
                                    >
                                        <AntDesign name="forward" size={40} color="white" />
                                    </TouchableOpacity>
                                </View>
                            </View>
                        </View>
                    </ImageBackground>
                </Animated.View>

                {
                    this.state.isExpanded ? null :
                        //collapsed player
                        <View style={{
                            position: 'absolute',
                            bottom: 50,
                            // backgroundColor: 'black',
                            overflow: 'hidden',
                            height: 50,
                            backgroundColor: 'black'
                        }}>
                            <Slider style={{ height: 0, width: '106%', left: '-3%' }}
                                thumbTintColor="rgba(0,0,0,0)"
                                minimumValue={0}
                                maximumValue={this.state.duration}
                                value={this.state.currentTime}
                                minimumTrackTintColor="#FF0054"
                            />
                            <TouchableOpacity style={styles.content}
                                onPress={this.expandPlayer}
                            >
                                <View style={styles.player}>
                                    <View style={{ width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
                                        <View style={styles.playBtnContainer}>
                                            <TouchableOpacity
                                                style={[styles.playBTN, { marginRight: 20 }]}
                                                onPress={this.onPressPlayPause}
                                            >
                                                {
                                                    this.state.playing
                                                        ?
                                                        <MaterialIcons name="pause" size={30} color="white" />
                                                        :
                                                        <Entypo name="controller-play" size={30} color="white" />
                                                }
                                            </TouchableOpacity>
                                            <View>
                                                {this.trackNameAmountOfSymbols > 23 ?
                                                    <View>
                                                        <TextTicker
                                                            style={[styles.text, { fontSize: 16 }]}
                                                            duration={10000}
                                                            loop
                                                            repeatSpacer={100}
                                                            marqueeDelay={1000}
                                                        >
                                                            {this.props.trackName}
                                                        </TextTicker>
                                                        <Text numberOfLines={1} style={[styles.text, { fontSize: 14, color: 'grey' }]}>{this.props.trackAuthor}</Text>
                                                    </View>
                                                    :
                                                    <View>
                                                        <Text numberOfLines={1} style={[styles.text, { fontSize: 16 }]}>{this.props.trackName}</Text>
                                                        <Text numberOfLines={1} style={[styles.text, { fontSize: 14, color: 'grey' }]}>{this.props.trackAuthor}</Text>
                                                    </View>
                                                }

                                            </View>
                                        </View>
                                        <TouchableOpacity style={{ height: '100%' }} onPress={async () => {
                                            this.setSongIsSaved(!this.state.songIsSaved)

                                            try {
                                                let path = 'http://192.168.1.66:12345/library/change_track_status/?library_id=' + 1 + '&track_id=' + PlayerQueue.getQueue.tracks[PlayerQueue.getCurrentTrack].id
                                                const callback = await fetch(
                                                    path,
                                                    {
                                                        method: 'POST',
                                                    }
                                                );

                                                return callback

                                            } catch (error) {
                                                console.error(error);
                                            }
                                        }}>
                                            {
                                                this.state.songIsSaved
                                                    ?
                                                    <AntDesign name="minuscircleo" size={24} color="white" />
                                                    :
                                                    <AntDesign name="pluscircleo" size={24} color="white" />
                                            }
                                        </TouchableOpacity>
                                    </View>



                                </View>
                            </TouchableOpacity>
                        </View>
                }
            </View>
        );
    };

})

const styles = StyleSheet.create({
    player: {
        display: 'flex',
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: "space-between",
        width: '100%',
    },
    content: {
        position: 'relative',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        height: 50,
        paddingHorizontal: 15
    },
    playBTN: {
        display: 'flex',
        flexDirection: 'flex-start',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1,
    },
    text: {
        color: 'white',
        fontSize: 20,
        fontFamily: 'Nunito-Bold',
        flexWrap: 'nowrap',
        overflow: 'hidden',
        width: 200,
    },
    playBtnContainer: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
    },
    trackPhoto: {
        width: 50,
        height: 50,
        borderRadius: '5%'
    },
    expandedContainerStyle: {
        height: '100%',
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-around',
        alignItems: 'center',
        paddingTop: '10%',
        paddingBottom: '15%',
        position: 'relative'
    },
    expandedControlBtns: {
        display: 'flex',
        flexDirection: 'row',
        justifyContent: "space-around",
        width: '80%',
        marginVertical: '5%'
    },
    expandedTrackInfo: {
        marginVertical: '10%',
        display: 'flex',
        width: '80%',
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center'
    },
    slider: {
        width: '100%',
        height: '10%',
    }
})