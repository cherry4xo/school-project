import React, { createRef, PureComponent, useRef } from "react";
import {
    View,
    StyleSheet,
    Text,
    Image,
    ImageBackground,
    Dimensions,
    TouchableOpacity,
    Animated
} from "react-native";
import Slider from '@react-native-community/slider'

import { Audio } from 'expo-av';
import { AntDesign, Entypo, MaterialIcons } from '@expo/vector-icons';
import DigitalTimeString from "./DigitalTimeString";

const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;

export default class AudioSlider extends PureComponent {

    constructor(props) {
        super(props);
        this.state = {
            playing: false,
            isExpanded: false,
            currentTime: 0, // miliseconds
            duration: 0,
            height: new Animated.Value(40)
        }

        this.setHeight = this.setHeight.bind(this)

        this.setTrackValue = this.setTrackValue.bind(this)

        this.expandPlayer = this.expandPlayer.bind(this)

        this.collapsPlayer = this.collapsPlayer.bind(this)
    };

    setHeight(value) {
        this.setState({ height: value })
    }

    setTrackValue(value) {
        this.setState({ trackValue: value })
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

    runSlider = async () => {
        if (this.state.playing && this.state.duration > this.state.currentTime + 1000) {
            let prevTime = this.state.currentTime
            this.setState({ currentTime: prevTime + 1000 })
        } else {
            //on end of the song function
            if (this.state.playing) {
                this.onPressPlayPause()
                // console.log('end of the song')
            }
        }
    }

    async componentDidMount() {
        this.soundObject = new Audio.Sound();
        await this.soundObject.loadAsync(this.props.audio);
        const status = await this.soundObject.getStatusAsync();
        this.setState({ duration: status["durationMillis"] });

        setInterval(this.runSlider, 1000);
    }

    async componentWillUnmount() {
        await this.soundObject.unloadAsync();
    }

    render() {
        return (
            <View style={{
            }}>
                {/* expanded player */}
                <Animated.View
                    style={{
                        height: windowHeight,
                        resizeMode: 'cover',
                        // top: -windowHeight + 35,
                        top: this.state.height,
                        width: windowWidth,
                        position: 'absolute',
                        zIndex: 2
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
                        source={this.props.trackIcon}
                    >
                        <View style={[styles.content, styles.expandedContainerStyle]}>
                            <TouchableOpacity style={{ position: 'absolute', right: 10, top: 10, zIndex: 1 }} onPress={this.collapsPlayer}>
                                <AntDesign name="close" size={35} color="white" />
                            </TouchableOpacity>

                            <View style={styles.expandedContainerStyle}>
                                <Image source={this.props.trackIcon} style={[styles.trackPhoto, {
                                    width: 300, height: 300
                                }]} />

                                <View style={styles.expandedTrackInfo}>
                                    <View>
                                        <Text numberOfLines={1} style={styles.text}>{this.props.trackName}</Text>
                                        <Text numberOfLines={1} style={[styles.text, { fontSize: 16 }]}>{this.props.trackAuthor}</Text>
                                    </View>
                                    <TouchableOpacity>
                                        <AntDesign name="pluscircleo" size={24} color="white" />
                                    </TouchableOpacity>

                                </View>

                                <Slider
                                    minimumValue={0}
                                    maximumValue={this.state.duration}
                                    step={1000}
                                    minimumTrackTintColor="red"
                                    style={[styles.slider, { width: '90%' }]}
                                    value={this.state.currentTime}
                                    onValueChange={
                                        currentTime => {
                                            this.setState({ currentTime })
                                            this.mapAudioToCurrentTime()
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
                                        onPress={() => { }}
                                    >
                                        <AntDesign name="banckward" size={40} color="white" />
                                    </TouchableOpacity>
                                    <TouchableOpacity
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
                                        onPress={() => { }}
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
                            backgroundColor: 'black',
                            overflow: 'hidden'
                        }}>
                            <Slider style={{ height: 0, width: '76%', left: '-2%' }}
                                thumbTintColor="rgba(0,0,0,0)"
                                minimumValue={0}
                                maximumValue={this.state.duration}
                                value={this.state.currentTime}
                                minimumTrackTintColor="red"
                            />
                            <TouchableOpacity style={styles.content}
                                onPress={this.expandPlayer}
                            >
                                <View style={styles.player}>

                                    <View style={styles.playBtnContainer}>
                                        <TouchableOpacity
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
                                        <View>
                                            <Text numberOfLines={1} style={[styles.text, { fontSize: 16 }]}>{this.props.trackName}</Text>
                                            <Text numberOfLines={1} style={[styles.text, { fontSize: 16 }]}>{this.props.trackAuthor}</Text>
                                        </View>
                                    </View>

                                    <Image source={this.props.trackIcon} style={styles.trackPhoto} />

                                </View>
                            </TouchableOpacity>
                        </View>
                }
            </View>
        );
    };

}

const styles = StyleSheet.create({
    player: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
        height: '100%',
        justifyContent: "space-between",
        width: '100%',
    },
    content: {
        position: 'relative',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        height: 75,
        paddingHorizontal: 15
    },
    playBTN: {
        display: 'flex',
        flexDirection: 'flex-start',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1,
        marginRight: 10
    },
    text: {
        color: 'white',
        fontSize: '20pt',
        fontFamily: 'Nunito-Bold',
        paddingVertical: 3,
        flexWrap: 'nowrap',
        overflow: 'hidden',
        maxWidth: 200,

    },
    playBtnContainer: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between'
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