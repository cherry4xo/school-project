import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, ScrollView, TouchableHighlight } from 'react-native';

export default function SearchPage({ navigation }) {

    const [value, setValue] = useState('')

    const [searchType, setSearchType] = useState('songs')

    return (
        <View style={styles.container}>
            <ScrollView
                contentContainerStyle={{ flexGrow: 1, alignItems: 'center', }}
                style={{ width: '100%', display: 'flex' }}
                keyboardShouldPersistTaps='handled'
            >
                <TextInput
                    style={styles.input}
                    value={value}
                    onChange={(event) => setValue(event.target.value)}
                    placeholder='Search'
                    placeholderTextColor={'white'}
                    keyboardAppearance='dark'
                />

                <View style={styles.searchTypes}>
                    <TouchableHighlight
                        style={(searchType == 'songs') ?
                            { borderBottomColor: 'white', borderWidth: 1 } :
                            { borderBottomColor: 'black', borderWidth: 1 }}
                        onPress={() => setSearchType('songs')}
                    >
                        <Text style={[styles.searchTypeText, (searchType == 'songs') ?
                            { color: 'white' } : { color: 'grey' }]}>
                            Songs
                        </Text>
                    </TouchableHighlight>
                    <TouchableHighlight
                        style={(searchType == 'albums') ?
                            { borderBottomColor: 'white', borderWidth: 1 } :
                            { borderBottomColor: 'black', borderWidth: 1 }}
                        onPress={() => setSearchType('albums')}
                    >
                        <Text style={[styles.searchTypeText, (searchType == 'albums') ?
                            { color: 'white' } : { color: 'grey' }]}>Albums</Text>
                    </TouchableHighlight>
                    <TouchableHighlight
                        style={(searchType == 'artists') ?
                            { borderBottomColor: 'white', borderWidth: 1 } :
                            { borderBottomColor: 'black', borderWidth: 1 }}
                        onPress={() => setSearchType('artists')}
                    >
                        <Text style={[styles.searchTypeText, (searchType == 'artists') ?
                            { color: 'white' } : { color: 'grey' }]}>Artists</Text>
                    </TouchableHighlight>

                </View>

                <View style={{ flex: 1, justifyContent: 'center' }}>
                    <Text style={styles.text}>
                        Search here!
                    </Text>
                </View>

            </ScrollView >
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
    }
})