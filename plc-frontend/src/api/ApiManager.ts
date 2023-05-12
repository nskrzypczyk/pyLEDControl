export const setEffect = async (effectName: string) => {
    const res = await fetch(`/effect/${effectName}`, {
        method: "POST",
        mode: "same-origin",
        headers: {
            "Content-Type": "application/json"
        }
    })
    return res.json()
}

export const getStatus = async () => {

}