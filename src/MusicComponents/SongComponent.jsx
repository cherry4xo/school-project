import React from "react";
import { useEffect } from "react";
import { useState } from "react";
import { StyleSheet, Text, View, TouchableHighlight, Image, ScrollView, Dimensions, } from 'react-native';

const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;

export default function SongComponent(props) {

    const [duration, setDuration] = useState('')
    const [authors, setAuthors] = useState('')

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
            setImage(URL.createObjectURL(data));
            return;
        } catch (error) {
            console.error(error)
        }
    };

    const [image, setImage] = useState(null)

    useEffect(() => {

        let min = Math.floor(props.duration / 60)
        let sec = (props.duration % 60)
        if (sec < 10) {
            sec = '0' + sec
        }
        setDuration(min + ':' + sec)

        let string = ''
        for (let i = 0; i < props.authors.length; i++) {
            string += props.authors[i].name + ' '
        }
        setAuthors(string)
        loadImage(props.id)
    }, [])
    return (
        <View>
            {
                props.showImage ?
                    <View style={styles.content}>
                        <Image
                            style={{ width: 40, height: 35, marginRight: 0, borderRadius: 3 }}
                            source={{ uri: image }}
                        />
                        <View style={{ width: '60%', fontSize: '18pt', marginHorizontal: 10, display: 'flex', flexDirection: 'column' }}>
                            <Text numberOfLines={1} style={[styles.text, { fontSize: '16pt' }]}>
                                {props.name}
                            </Text>
                            <Text numberOfLines={1} style={[styles.text, { fontSize: '14pt', color: 'grey' }]}>
                                {authors}
                            </Text>
                        </View>

                        <Text numberOfLines={1} style={[styles.text, { width: '20%', color: '#FF0054', fontFamily: 'Nunito-Bold', fontSize: '16pt' }]}>
                            {duration}
                        </Text>
                    </View>
                    :
                    <View style={styles.content}>
                        <Text numberOfLines={1} style={[styles.text, { width: '70%', fontSize: '18pt' }]}>
                            {props.name}
                        </Text>
                        <Text numberOfLines={1} style={[styles.text, { width: '20%', color: '#FF0054', fontFamily: 'Nunito-Bold', fontSize: '16pt' }]}>
                            {duration}
                        </Text>
                    </View>
            }

        </View>
    );
}

const styles = StyleSheet.create({
    content: {
        width: windowWidth - 20,
        display: 'flex',
        flexDirection: 'row',
        height: 45,
        // marginVertical: 10,
        paddingLeft: 30,
        alignItems: 'center',
        justifyContent: 'space-between'
        // borderColor: 'white',
        // borderWidth: 1,
        // borderRadius: 5
    },
    text: {
        color: 'white',
        maxWidth: windowWidth,
        fontFamily: 'Nunito-Medium',
        fontSize: 20,
        overflow: 'hidden',
    },
})