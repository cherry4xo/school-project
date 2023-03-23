import React from 'react';
import { StyleSheet, Text, FlatList, View, TouchableHighlight, ScrollView } from 'react-native';

import Album from '../MusicComponents/AlbumComponent.jsx'

import { useState, useEffect } from 'react';

export default function LibraryAlbums() {

    function AlbumsList() {
        if (albumsList.length > 0) {
            return (
                < View style={[styles.Albums, { justifyContent: 'center' }]}>
                    {
                        albumsList.map((item) => {
                            return (
                                <Album
                                    key={item.album_data.id}
                                    id={item.album_data.id}
                                    albumName={item.album_data.name}
                                    authors={item.artists}
                                />
                            )
                        }
                        )
                    }
                    {
                        (albumsList.length % 2 != 0) ?
                            <View style={{ width: 140, marginHorizontal: 20 }} />
                            :
                            null
                    }
                </View >
            );
        } else {
            return (
                <View></View>
            )
        }

    }

    const fetchAlbumsList = async (id) => {
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

    const getAlbumsList = async (id) => {
        let list = await fetchAlbumsList(id)
        setAlbumsList(list.albums.reverse())
    }

    const [albumsList, setAlbumsList] = useState([])

    useEffect(() => {
        const get = async () => {
            await getAlbumsList(1)
        }

        get()
    }, [])

    return (
        <View style={{ backgroundColor: 'black' }}>
            <ScrollView contentContainerStyle={styles.container}>
                <AlbumsList />
            </ScrollView >
        </View>

    )
}

const styles = StyleSheet.create({
    container: {
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
    menuItem: {
        display: 'flex',
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'flex-start',
        width: '100%',
        margin: 8,
    },
    line: {
        borderBottomWidth: 1,
        borderBottomColor: '#5A5A5A',
        width: '80%',
    },
    Albums: {
        flexDirection: 'row',
        gap: '1rem',
        flexWrap: "wrap",
        width: '100%',
        display: 'flex',
    },
})