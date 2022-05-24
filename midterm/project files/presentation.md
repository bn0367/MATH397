Isometric projection matrix:\
$\begin{bmatrix}1&0&0\\0&\cos\alpha&\sin\alpha\\0&-\sin\alpha&-\cos\alpha\end{bmatrix}
\cdot
\begin{bmatrix}\cos\beta&0&-\sin\beta\\0&1&0\\\sin\beta&0&\cos\beta\end{bmatrix}$  
\
\
Perspective projection matrix: 
$$\begin{bmatrix}1&0&0\\0&\cos\theta_x&\sin\theta_x\\0&-\sin\theta_x&\cos\theta_x\end{bmatrix}\cdot\begin{bmatrix}\cos\theta_y&0&-\sin\theta_y\\0&1&0\\\sin\theta_y&0&\cos\theta_y\end{bmatrix}\cdot\begin{bmatrix}\cos\theta_z&\sin\theta_z&0\\-\sin\theta_z&\cos\theta_z&0\\0&0&1\end{bmatrix}\cdot\left(\begin{bmatrix}p_x\\p_y\\p_z\end{bmatrix}-\begin{bmatrix}c_x\\c_y\\c_z\end{bmatrix}\right)$$