import React, { useState } from 'react';
import { useEffect } from 'react';
import { StyleSheet, Text, View, Button, TextInput, ScrollView, TouchableHighlight } from 'react-native';
import Song from '../MusicComponents/SongComponent'
import Album from '../MusicComponents/AlbumComponent';
import { PlayerQueue } from '../mobX/playerQUEUE';

export default function SearchPage(props) {

    const setSongAsQueue = async (track) => {
        const loadSong = async (id) => {
            try {
                const res = await fetch(
                    'http://192.168.1.66:12345/track/get_picture/' + id,
                    {
                        method: 'GET',
                        cache: 'no-cache'
                    }
                )
                const data = await res.blob();
                return URL.createObjectURL(data)
            } catch (error) {
                console.error(error)
            }
        };

        let artistsString = ''
        for (let i = 0; i < track.artists.length; i++) {
            artistsString += track.artists[i].name + ' '
        }
        let song = await loadSong(track.track_data.id)
        console.log(song)
        let post = [{
            "artists": [
                artistsString
            ],
            "name": track.track_data.name,
            "id": track.track_data.id,
        }]
        PlayerQueue.setCurrentTrack(0)
        PlayerQueue.changeQueue(post)
    }

    function SearchBlock(props) {

        function SongsList() {
            if (songsList.length > 0) {
                return (
                    <View>
                        <View style={[styles.line, { width: '100%' }]} />
                        {
                            songsList.map((item) => {
                                return (
                                    <View key={item.track_data.id}>
                                        <TouchableHighlight onPress={() => { setSongAsQueue(item) }}>
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
                        <Text style={styles.text}>No such song in database</Text>
                    </View>
                )
            }

        }

        function AlbumsList() {
            if (albumsList.length > 0) {
                return (
                    < View style={[styles.Albums, { justifyContent: 'center' }]}>
                        {
                            albumsList.map((item) => {
                                return (
                                    <Album key={item.album_data.id} id={item.album_data.id} albumName={item.album_data.name} authors={item.artists} />
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
                    <View style={{ display: 'flex', justifyContent: "center", alignItems: 'center' }}>
                        <Text style={styles.text}>No such album in database</Text>
                    </View>
                )
            }

        }

        if (props.searchType == 'track') {
            return (
                <SongsList />
            )
        }
        if (props.searchType == 'album') {
            return (
                <AlbumsList />
            )
        }
    }

    const fetchSongsList = async (searchText) => {
        try {
            let path = 'http://192.168.1.66:12345/page/search/?search_str=' + searchText + '&search_page=' + searchType
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

    const fetchAlbumsList = async (searchText) => {
        try {
            let path = 'http://192.168.1.66:12345/page/search/?search_str=' + searchText + '&search_page=' + searchType
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

    const getAlbumsList = async (text) => {
        let list = await fetchAlbumsList(text)
        setAlbumsList(list)
        setShowList(true)
    }

    const getSongsList = async (text) => {
        let list = await fetchSongsList(text)
        setSongsList(list)
        setShowList(true)
    }

    const changeText = async (text) => {
        if (searchType == 'track') {
            await getSongsList(text)
        }
        if (searchType == 'album') {
            await getAlbumsList(text)
        }
    }

    const [showList, setShowList] = useState(false)
    const [songsList, setSongsList] = useState([])
    const [albumsList, setAlbumsList] = useState([])
    const [searchType, setSearchType] = useState('track')
    const [text, setText] = useState('')

    useEffect(() => {
        const inputSearch = async () => {
            if (text.length >= 2) {
                await changeText(text)
            } else {
                setShowList(false)
            }
        }
        inputSearch()
    }, [text])

    return (
        <View style={styles.container}>
            <ScrollView
                contentContainerStyle={{ flexGrow: 1, alignItems: 'center', }}
                style={{ width: '100%', display: 'flex' }}
                keyboardShouldPersistTaps='handled'
            >
                <TextInput
                    style={styles.input}
                    value={text}
                    onChangeText={async input => {
                        setText(input)
                    }
                    }
                    placeholder='Search'
                    placeholderTextColor={'white'}
                    keyboardAppearance='dark'
                />

                <View style={styles.searchTypes}>
                    <TouchableHighlight
                        style={(searchType == 'track') ?
                            { borderBottomColor: '#FF0054', borderWidth: 1 } :
                            { borderBottomColor: 'black', borderWidth: 1 }}
                        onPress={async () => {
                            setSearchType('track')
                            setText('')
                        }
                        }
                    >
                        <Text style={[styles.searchTypeText, (searchType == 'track') ?
                            { color: '#FF0054' } : { color: 'grey' }]}>
                            Songs
                        </Text>
                    </TouchableHighlight>
                    <TouchableHighlight
                        style={(searchType == 'album') ?
                            { borderBottomColor: '#FF0054', borderWidth: 1 } :
                            { borderBottomColor: 'black', borderWidth: 1 }}
                        onPress={async () => {
                            setSearchType('album')
                            setText('')
                        }
                        }
                    >
                        <Text style={[styles.searchTypeText, (searchType == 'album') ?
                            { color: '#FF0054' } : { color: 'grey' }]}>Albums</Text>
                    </TouchableHighlight>
                    <TouchableHighlight
                        style={(searchType == 'artist') ?
                            { borderBottomColor: '#FF0054', borderWidth: 1 } :
                            { borderBottomColor: 'black', borderWidth: 1 }}
                        onPress={async () => {
                            setSearchType('artist')
                            await getList()
                        }
                        }
                    >
                        <Text style={[styles.searchTypeText, (searchType == 'artist') ?
                            { color: '#FF0054' } : { color: 'grey' }]}>Artists</Text>
                    </TouchableHighlight>
                </View>

                <View style={{ flex: 1, justifyContent: 'center' }}>
                    <Text style={styles.text}>
                        Search here!
                    </Text>
                </View>
            </ScrollView >
            {showList ?
                <ScrollView style={styles.SearchBlock}>
                    <SearchBlock searchType={searchType} />
                </ScrollView>
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
        alignItems: 'center'
    },
    text: {
        color: 'white',
        fontFamily: 'Nunito-Bold',
        fontSize: '20pt'
    },
    input: {
        width: '90%',
        height: 35,
        borderRadius: 10,
        backgroundColor: '#5A5A5A',

        paddingHorizontal: '5%',

        color: 'white',
        fontFamily: 'Nunito-Regular',
        fontSize: '18pt'
    },
    searchTypes: {
        flexDirection: 'row',
        width: '100%',
        justifyContent: 'space-around'
    },
    searchTypeText: {
        fontFamily: 'Nunito-Bold',
        fontSize: '18pt',
        margin: 10,
    },
    SearchBlock: {
        backgroundColor: 'black',
        position: 'absolute',
        width: '100%',
        height: '100%',
        top: 100
    },
    line: {
        borderBottomWidth: 1,
        // borderBottomColor: '#5A5A5A',
        borderBottomColor: 'grey',
    },
    Albums: {
        flexDirection: 'row',
        gap: '1rem',
        flexWrap: "wrap",
        width: '100%',
        display: 'flex',
    }
})