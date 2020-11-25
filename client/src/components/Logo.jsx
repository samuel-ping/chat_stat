import "./Logo.css"

function Logo(props) {
    return (
        <>
            <div className="logo-wrapper">
                <div className={props.isAnimated ? "typing-effect" : ""}>
                    <div className={props.isAnimated ? "blinking-cursor" : ""}>
                        chat_stat
                    </div>
                </div>
            </div> 
        </>
    );
}

export default Logo;