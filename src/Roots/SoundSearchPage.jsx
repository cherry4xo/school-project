import React, { useEffect } from 'react';
import { useState } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Image, Animated } from 'react-native';
import {
    MaterialIndicator,
    PulseIndicator,
} from 'react-native-indicators';

import { AntDesign, Entypo, MaterialIcons } from '@expo/vector-icons';

import { Dimensions } from 'react-native';

const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;

export default function SoundSearchPage({ navigation }) {

    const [loading, setLoading] = useState(false)
    const [isExpanded, setIsExpanded] = useState(true)
    const [height, setHeight] = useState(new Animated.Value(windowHeight))

    async function search() {
        setLoading(true)
        getSongInfo(1)
        setTimeout(() => {
            expandPlayer()
            setLoading(false)
        }, 10000);
    }

    const expandPlayer = () => {
        Animated.timing(height, {
            toValue: 0,
            useNativeDriver: false,
            duration: 400
        }).start()
        setIsExpanded(true)
    }

    const collapsPlayer = () => {
        Animated.timing(height, {
            toValue: windowHeight,
            useNativeDriver: false,
            duration: 400
        }).start()
        setIsExpanded(false)
    }

    const loadSongName = (id) => {
        return 'Smells Like Teen Spirit'
    }

    const loadImage = async (id) => {
        try {
            const res = await fetch(
                'http://192.168.1.66:12345/track/get_picture/' + id,
                {
                    method: 'GET',
                    cache: 'no-cache'
                }
            )
            const data = await res.blob();
            return URL.createObjectURL(data);
        } catch (error) {
            console.error(error)
        }
    };

    const loadSongAuthor = (id) => {
        return 'Nirvana'
    }

    const getSongInfo = async (id) => {

        let img = await loadImage(id)
        let song = loadSongName(id)
        let author = loadSongAuthor(id)

        setSongName(song)
        setImage(img)
        setSongAuthor(author)
    }

    const [image, setImage] = useState(null)
    const [songName, setSongName] = useState('')
    const [songAuthor, setSongAuthor] = useState('')

    return (
        <View style={styles.container}>

            <Animated.View style={{ backgroundColor: 'black', width: '100%', height: '100%', zIndex: 2, top: height, display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <TouchableOpacity style={{ position: 'absolute', right: 10, top: 10, zIndex: 1 }} onPress={collapsPlayer}>
                    <AntDesign name="close" size={35} color="white" />
                </TouchableOpacity>
                <Image
                    source={{ uri: image }}
                    style={[styles.trackPhoto, {
                        width: 300, height: 300, borderRadius: '5%'
                    }]} />
                <Text style={[styles.text, { marginVertical: 25 }]}>Song:{' ' + songName}</Text>
                <Text style={styles.text}>Artist:{' ' + songAuthor}</Text>
            </Animated.View>

            <Text style={[styles.text, { marginVertical: 25 }]}>Sound search page</Text>
            <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                <TouchableOpacity onPress={search} style={styles.searchButotn}>
                    <Text style={styles.text}>Find song</Text>
                </TouchableOpacity>
            </View>

            {
                loading ?
                    <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                        <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                            <MaterialIndicator trackWidth={10} size={220} color='#FF8C3E' />
                        </View>
                        {/* <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                            <MaterialIndicator size={220} color='blue' />
                        </View> */}
                        <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                            <MaterialIndicator size={200} color='#FF5D3E' />
                        </View>
                        <View style={{ position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, justifyContent: 'center', alignItems: 'center' }}>
                            <PulseIndicator size={300} color='#FF5D00' />
                        </View>
                    </View>
                    :
                    null
            }
        </View >
    )
}

const styles = StyleSheet.create({

    container: {
        width: '100%',
        height: '100%',
        flex: 1,
        backgroundColor: 'black',
        display: 'flex',
        alignItems: 'center',
    },
    text: {
        color: 'white',
        fontFamily: 'Nunito-Bold',
        fontSize: '20pt'
    },
    searchButotn: {
        width: 200,
        height: 200,
        borderRadius: 200 / 2,
        backgroundColor: '#FF0054',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    }
})