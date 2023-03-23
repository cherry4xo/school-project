import React from 'react';
import { useEffect } from 'react';
import { useState } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableHighlight } from 'react-native';
import Song from '../MusicComponents/SongComponent'
import { PlayerQueue } from '../mobX/playerQUEUE';

export default function RecPage({ navigation }) {

    const setSongAsQueue = async (index) => {

        let post = []

        for (let i = 0; i < songsList.length; i++) {
            let track = songsList[i]
            let artistsString = ''
            for (let i = 0; i < track.artists.length; i++) {
                artistsString += track.artists[i].name + ' '
            }

            post.push({
                "added": track.added,
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

    const fetchSongsList = async (id) => {
        try {
            let path = 'http://192.168.1.66:12345/recommendations/get_recs_by_library_tracks/' + id
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
        setSongsList(list)
    }

    const [songsList, setSongsList] = useState([])

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
                </View >
            );
        } else {
            return (
                <View style={{ display: 'flex', justifyContent: "center", alignItems: 'center' }}>
                </View>
            )
        }

    }

    useEffect(() => {
        getSongsList(1)
    }, [])

    return (
        <View style={{ backgroundColor: 'black', width: '100%', height: '100%', flex: 1 }}>
            <ScrollView contentContainerStyle={styles.scroll}>
                <Text style={[styles.text, { marginVertical: 25 }]}>Your suggestion list:</Text>
                <SongsList />
            </ScrollView>
        </View>

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
    line: {
        borderBottomWidth: 1,
        borderBottomColor: '#5A5A5A',
    },
    scroll: {
        width: '100%',
        minHeight: '100%',
        backgroundColor: 'black',
        alignItems: 'center',
        display: 'flex',
        paddingBottom: 50
    }
})