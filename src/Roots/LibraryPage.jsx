import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { createNativeStackNavigator } from '@react-navigation/native-stack';

//components
import LibraryStart from '../LibraryComponents/LibraryStart';
import LibrarySongs from '../LibraryComponents/LibrarySongs';
import LibraryAlbums from '../LibraryComponents/LibraryAlbums';
import LibraryPlaylists from '../LibraryComponents/LibraryPlaylists';

import AlbumPage from '../MusicComponents/AlbumPage'

const LibraryStack = createNativeStackNavigator();

export default function LibraryPage({ navigation }) {
    return (
        <LibraryStack.Navigator initialRouteName='LibraryMenu'>
            <LibraryStack.Screen
                name='LibraryMenu'
                component={LibraryStart}
                options={{
                    title: 'Library',
                    headerStyle: {
                        backgroundColor: 'black',
                        elevation: 0,
                        shadowOffset: {
                            width: 0,
                            height: 0
                        }

                    },
                    headerTintColor: 'white',
                    headerTitleStyle: {
                        fontFamily: 'Nunito-Bold',
                    },
                }}
            />
            <LibraryStack.Screen
                name='Songs'
                component={LibrarySongs}
                options={{
                    title: 'Songs',
                    headerStyle: {
                        backgroundColor: 'black',
                        elevation: 0,
                        shadowOffset: {
                            width: 0,
                            height: 0
                        }

                    },
                    headerTintColor: 'white',
                    headerTitleStyle: {
                        fontFamily: 'Nunito-Bold',
                    },
                }}
            />
            <LibraryStack.Screen
                name='Albums'
                component={LibraryAlbums}
                options={{
                    title: 'Albums',
                    headerStyle: {
                        backgroundColor: 'black',
                        elevation: 0,
                        shadowOffset: {
                            width: 0,
                            height: 0
                        }

                    },
                    headerTintColor: 'white',
                    headerTitleStyle: {
                        fontFamily: 'Nunito-Bold',
                    },
                }}
            />
            <LibraryStack.Screen
                name='Playlists'
                component={LibraryPlaylists}
                options={{
                    title: 'Playlists',
                    headerStyle: {
                        backgroundColor: 'black',
                        elevation: 0,
                        shadowOffset: {
                            width: 0,
                            height: 0
                        }

                    },
                    headerTintColor: 'white',
                    headerTitleStyle: {
                        fontFamily: 'Nunito-Bold',
                    },
                }}
            />
            <LibraryStack.Screen
                name='AlbumPage'
                component={AlbumPage}
                options={{
                    title: '',
                    headerStyle: {
                        backgroundColor: 'black',
                        elevation: 0,
                        shadowOffset: {
                            width: 0,
                            height: 0
                        }
                    },
                    headerTintColor: 'white',
                    headerTitleStyle: {
                        fontFamily: 'Nunito-Bold',
                    },
                }}
            />
        </LibraryStack.Navigator>
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
        justifyContent: 'center'
    },
    text: {
        color: 'white',
        fontFamily: 'Nunito-Bold',
        fontSize: '20pt'
    }
})