import React from "react";
import { useState } from "react";
import { useEffect } from "react";
import { StyleSheet, Text, View, Image, TouchableHighlight, ScrollView, Dimensions, Button } from 'react-native';
import { AlbumPageParams } from "../mobX/albumPage.js";
import { useFocusEffect } from '@react-navigation/native';
import { useNavigation } from '@react-navigation/native';

import Song from './SongComponent.jsx'

import { PlayerQueue } from "../mobX/playerQUEUE.js";

const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;

export default function AlbumPage({ navigation }) {

    const setSongAsQueue = async (index) => {

        let post = []

        for (let i = 0; i < DATA.tracks.length; i++) {
            let track = DATA.tracks[i]
            let artistsString = ''
            for (let i = 0; i < track.artists.length; i++) {
                artistsString += track.artists[i].name + ' '
            }

            post.push({
                "artists": [
                    artistsString
                ],
                "name": track.track_data.name,
                "id": track.track_data.id,
            })
        }

        PlayerQueue.setCurrentTrack(index)
        PlayerQueue.changeQueue(post)
    }

    function SongsList() {
        return (
            <View>
                <View style={[styles.line, { width: '100%' }]} />
                {
                    DATA.tracks.map((item, index) => {
                        return (
                            <View key={item.track_data.id}>
                                <TouchableHighlight onPress={() => { setSongAsQueue(index) }}>
                                    <View>
                                        <Song
                                            showImage={false}
                                            id={item.track_data.id}
                                            authors={item.artists}
                                            duration={item.track_data.duration_s}
                                            name={item.track_data.name}
                                        />
                                    </View>
                                </TouchableHighlight>
                                <View style={[styles.line, { width: '100%' }]} />

                            </View>
                        )
                    }
                    )
                }
            </View >

        );
    }

    const fetchAlbumImage = async () => {
        try {
            let path = 'http://192.168.1.66:12345/album/get_picture/' + AlbumPageParams.getParams
            const res = await fetch(
                path,
                {
                    method: 'GET',
                    headers: {
                        Accept: 'image/*',
                        'Content-Type': 'image/*',
                    },
                    cache: 'no-cache'
                }
            );
            const imageBlob = await res.blob();
            const callback = URL.createObjectURL(imageBlob);
            setImage(callback)
            return

        } catch (error) {
            console.error(error);
        }
    };

    const fetchAlbumData = async (library_id) => {
        try {
            let path = 'http://192.168.1.66:12345/page/album/' + AlbumPageParams.getParams + '?library_id=' + library_id
            const res = await fetch(
                path,
                {
                    method: 'GET',
                    headers: {
                        Accept: 'application/json',
                        'Content-Type': 'application/json',
                    },
                }
            );
            const callback = await res.json()
            setDATA(callback)
            return

        } catch (error) {
            console.error(error);
        }
    };

    const getData = async (id) => {
        await fetchAlbumData(id)
        await fetchAlbumImage()
    }

    const [image, setImage] = useState(null)
    const [DATA, setDATA] = useState(null)

    useFocusEffect(
        React.useCallback(() => {
            const get = async () => {
                await getData(1)
            }
            get()
        }, [])
    )

    return (
        <View style={{ backgroundColor: 'black', flex: 1 }}>
            {
                (DATA == null || image == null) ? null :
                    <ScrollView contentContainerStyle={styles.content}>
                        <Image style={styles.image} source={{ uri: image }} />
                        <View style={{ width: '80%', marginTop: 10 }}>
                            <Text
                                numberOfLines={1}
                                style={[
                                    styles.text,
                                    {
                                        fontSize: 30,
                                        display: 'flex',
                                        alignSelf: 'center'
                                    }
                                ]}
                            >
                                {DATA.album_data.name}
                            </Text>
                        </View>
                        <View style={{ width: '80%', marginBottom: 20, }}>
                            <Text
                                numberOfLines={1}
                                style={[
                                    styles.text,
                                    {
                                        color: '#FF0054',
                                        display: 'flex',
                                        alignSelf: 'center'
                                    }
                                ]}
                            >
                                {DATA.artists[0].name}
                            </Text>
                        </View>

                        {/* List of songs */}
                        <SongsList />
                        <View style={{ width: '100%', paddingHorizontal: 30, display: 'flex', flexDirection: 'row' }}>
                            <Text style={[styles.text, { fontFamily: 'Nunito-Light', color: 'grey', fontSize: '16pt', marginTop: 10, marginBottom: 50 }]}>
                                Number of songs : { }
                            </Text>
                            <Text style={[styles.text, { color: '#FF0054', fontSize: '16pt', marginTop: 10, marginBottom: 50 }]}>
                                {DATA.tracks.length}
                            </Text>
                        </View>
                    </ScrollView>
            }

        </View>
    );
}

const styles = StyleSheet.create({
    content: {
        width: '100%',
        minHeight: '100%',
        backgroundColor: 'black',
        alignItems: 'center',
        display: 'flex',
        paddingBottom: 50
    },
    text: {
        color: 'white',
        fontFamily: 'Nunito-Bold',
        fontSize: '20pt',
        overflow: 'hidden',
    },
    line: {
        borderBottomWidth: 1,
        borderBottomColor: '#5A5A5A',
    },
    image: {
        borderRadius: 10,
        // backgroundColor: "#7cb48f", 
        borderColor: '#5A5A5A',
        borderWidth: 1,
        width: 300,
        height: 300,
    }
})