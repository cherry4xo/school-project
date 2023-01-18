import React, { PureComponent } from "react";
import {
    View,
    StyleSheet,
    Text,
    Image,
    TouchableOpacity
} from "react-native";
import { Audio } from 'expo-av';
import { AntDesign, Entypo, MaterialIcons } from '@expo/vector-icons';

const TRACK_SIZE = 4;
const THUMB_SIZE = 20;


export default class AudioSlider extends PureComponent {

    constructor(props) {
        super(props);
        this.state = {
            playing: false,
            isExpanded: false,
        }

        this.expandPlayer = this.expandPlayer.bind(this)

        this.collapsPlayer = this.collapsPlayer.bind(this)

    };

    expandPlayer() {
        this.setState({ isExpanded: true })
    }

    collapsPlayer() {
        this.setState({ isExpanded: false })
    }

    onPressPlayPause = async () => {
        if (this.state.playing) {
            await this.pause();
            return
        }
        await this.play();
    }

    play = async () => {
        await this.soundObject.playAsync();
        this.setState({ playing: true }) // This is for the play-button to go to play
    }

    pause = async () => {
        await this.soundObject.pauseAsync();
        this.setState({ playing: false }) // This is for the play-button to go to pause
    }

    async componentDidMount() {
        this.soundObject = new Audio.Sound();
        await this.soundObject.loadAsync(this.props.audio);
    }

    async componentWillUnmount() {
        await this.soundObject.unloadAsync();
    }

    render() {
        return (
            <View>
                {
                    this.state.isExpanded ?
                        <View style={[styles.content, this.state.isExpanded ? styles.expandedContainerStyle : null]}
                        >
                            <TouchableOpacity style={{ position: 'absolute', right: 10, top: 10, zIndex: 1 }} onPress={this.collapsPlayer}>
                                <AntDesign name="close" size={35} color="white" />
                            </TouchableOpacity>

                            <View style={styles.expandedContainerStyle}>
                                <Image source={this.props.trackIcon} style={[styles.trackPhoto, { width: 300, height: 300 }]} />

                                <View style={styles.expandedTrackInfo}>
                                    <View>
                                        <Text numberOfLines={1} style={[styles.text, { fontSize: 16 }]}>{this.props.trackName}</Text>
                                        <Text numberOfLines={1} style={styles.text}>{this.props.trackAuthor}</Text>
                                    </View>
                                    <TouchableOpacity>
                                        <AntDesign name="pluscircleo" size={24} color="white" />
                                    </TouchableOpacity>

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
                        </View> :
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
                                        <Text numberOfLines={1} style={styles.text}>{this.props.trackName}</Text>
                                        <Text numberOfLines={1} style={styles.text}>{this.props.trackAuthor}</Text>
                                    </View>
                                </View>

                                <Image source={this.props.trackIcon} style={styles.trackPhoto} />

                            </View>
                        </TouchableOpacity>
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
        zIndex: 2,
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
        paddingTop: '8%',
        paddingBottom: '20%',
        position: 'relative'
    },
    expandedControlBtns: {
        display: 'flex',
        flexDirection: 'row',
        justifyContent: "space-around",
        alignItems: 'center',
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
    }
})