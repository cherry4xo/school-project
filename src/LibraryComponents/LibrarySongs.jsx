import React from "react";
import { useEffect, useState } from "react";
import { StyleSheet, Text, View, Image, TouchableHighlight, ScrollView, Dimensions } from 'react-native';

import Song from '../MusicComponents/SongComponent'

import { PlayerQueue } from "../mobX/playerQUEUE";

const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;

export default function LibrarySongs(props) {

    const setSongAsQueue = async (index) => {

        let post = []

        for (let i = 0; i < songsList.length; i++) {
            let track = songsList[i]
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
        if (songsList.length > 0) {
            return (
                <View>
                    <View style={[styles.line, { width: '100%' }]} />
                    {
                        songsList.map((item, index) => {
                            return (
                                <View key={item.track_data.id}>
                                    <TouchableHighlight onPress={() => { setSongAsQueue(index) }}>
                                        <View>
                                            <Song
                                                showImage={true}
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
                    <View style={{ width: '100%', paddingHorizontal: 30, display: 'flex', flexDirection: 'row' }}>
                        <Text style={[styles.text, { fontFamily: 'Nunito-Light', color: 'grey', fontSize: '16pt', marginTop: 10, marginBottom: 50 }]}>
                            Number of songs : { }
                        </Text>
                        <Text style={[styles.text, { color: '#FF0054', fontSize: '16pt', marginTop: 10, marginBottom: 50 }]}>
                            {songsList.length}
                        </Text>
                    </View>
                </View >
            );
        } else {
            return (
                <View style={{ display: 'flex', justifyContent: "center", alignItems: 'center' }}>

                </View>
            )
        }

    }

    const fetchSongsList = async (id) => {
        try {
            let path = 'http://192.168.1.66:12345/library/?library_id=' + id
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

            return callback

        } catch (error) {
            console.error(error);
        }
    };

    const getSongsList = async (id) => {
        let list = await fetchSongsList(id)
        setSongsList(list.tracks.reverse())
    }

    const [songsList, setSongsList] = useState([])

    useEffect(() => {
        const get = async () => {
            await getSongsList(1)
        }

        get()
    }, [])

    return (
        <View style={{ backgroundColor: 'black', flex: 1 }}>
            <ScrollView contentContainerStyle={styles.content}>
                {/* List of songs */}
                <SongsList />
            </ScrollView>
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