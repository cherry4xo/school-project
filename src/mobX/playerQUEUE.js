import { action, computed, makeObservable, observable, toJS } from "mobx"

class PlayerQueueMobx {
    currentTrack = 0
    queue = {
        "tracks": [
        ]
    }

    constructor() {
        makeObservable(this, {
            queue: observable,
            changeQueue: action,
            getQueue: computed,
            currentTrack: observable,
            increaseCurrentTrack: action,
            decreaseCurrentTrack: action,
            setCurrentTrack: action,
            getCurrentTrack: computed,
            getCurrentImage: computed,
            isAlone: computed
        })
    }

    changeQueue(newQueue) {
        this.queue.tracks = newQueue
    }

    get isAlone() {
        return this.queue.tracks.length == 1
    }

    get getCurrentImage() {
        return this.queue.tracks[this.currentTrack].image
    }

    get getQueue() {
        return this.queue
    }

    setCurrentTrack = (pos) => {
        this.currentTrack = pos
    }

    increaseCurrentTrack = () => {
        if (this.currentTrack + 1 >= this.queue.tracks.length) {
            this.currentTrack = 0
        }
        else {
            this.currentTrack++
        }
    }

    decreaseCurrentTrack = () => {
        if (this.currentTrack - 1 < 0) {
            this.currentTrack = this.queue.tracks.length - 1
        } else {
            this.currentTrack--
        }
    }

    get getCurrentTrack() {
        return this.currentTrack
    }

}

export const PlayerQueue = new PlayerQueueMobx()